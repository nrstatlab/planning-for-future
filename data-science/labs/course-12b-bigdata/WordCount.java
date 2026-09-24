// Experiment 7 -- word count in MapReduce
//
// *** NOT EXECUTED ***
// This is the Java MapReduce program you compile and submit on a real cluster.
// Hadoop cannot be installed in the verification environment -- the Debian
// repositories that host it are blocked by the egress policy -- so this file
// has never been compiled or run here. Nothing in the notes claims an output
// for it.
//
// The runnable half is 07_wordcount.py, which runs the same map and reduce
// functions through an explicit engine and asserts every count
//
// Build and run:
//   javac -classpath $(hadoop classpath) -d classes WordCount.java
//   jar -cvf WordCount.jar -C classes/ .
//   hadoop jar WordCount.jar WordCount /user/student/docs /user/student/out
//

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WordCount {

    public static class TokenizerMapper
            extends Mapper<LongWritable, Text, Text, IntWritable> {

        // Reused across every call. Allocating a new Text per word would
        // create one object per word in the corpus, and the GC pause is the
        // job. This is the single most important idiom in MapReduce Java.
        private final static IntWritable ONE = new IntWritable(1);
        private final Text word = new Text();

        @Override
        public void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {
            // key is the BYTE OFFSET of the line, not a line number.
            StringTokenizer itr = new StringTokenizer(value.toString());
            while (itr.hasMoreTokens()) {
                word.set(itr.nextToken().toLowerCase());
                context.write(word, ONE);
            }
        }
    }

    public static class IntSumReducer
            extends Reducer<Text, IntWritable, Text, IntWritable> {

        private final IntWritable result = new IntWritable();

        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context)
                throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            // The Iterable is streamed from disk and can be walked ONCE.
            // Calling values.iterator() a second time yields nothing -- the
            // classic bug when someone tries to compute a mean and a count.
            result.set(sum);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "word count");
        job.setJarByClass(WordCount.class);

        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);   // safe: sum is associative
        job.setReducerClass(IntSumReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        job.setNumReduceTasks(1);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        // The output directory MUST NOT EXIST. Hadoop refuses to overwrite,
        // which prevents a re-run from silently destroying yesterday's result.

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

// Expected output on the six sample documents (verified in 07_wordcount.py):
//   the 5,  big 4,  data 4,  dog 4,  fox 3,  quick 3,  ... 26 terms, 48 words
//
// The combiner is the same class as the reducer here ONLY because sum is
// associative and commutative. Setting a combiner for a mean silently
// produces wrong answers -- mean of means is not the mean -- and Hadoop will
// not warn you.
