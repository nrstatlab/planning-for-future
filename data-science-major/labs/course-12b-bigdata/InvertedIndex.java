// Experiment 8 -- an inverted index in MapReduce
//
// *** NOT EXECUTED ***
// This is the Java MapReduce program you compile and submit on a real cluster.
// Hadoop cannot be installed in the verification environment -- the Debian
// repositories that host it are blocked by the egress policy -- so this file
// has never been compiled or run here. Nothing in the notes claims an output
// for it.
//
// The runnable half is 08_inverted_index.py, which builds the same index and
// answers boolean queries against it
//
// Build and run:
//   javac -classpath $(hadoop classpath) -d classes InvertedIndex.java
//   jar -cvf InvertedIndex.jar -C classes/ .
//   hadoop jar InvertedIndex.jar InvertedIndex /user/student/docs /user/student/out
//

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.StringTokenizer;
import java.util.TreeMap;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class InvertedIndex {

    public static class IndexMapper
            extends Mapper<LongWritable, Text, Text, Text> {

        private final Text word = new Text();
        private final Text docId = new Text();
        private String fileName;

        @Override
        protected void setup(Context context) {
            // THE FILENAME IS NOT IN THE KEY OR THE VALUE. It comes from the
            // InputSplit, and this is the only way to get at it. Every
            // inverted-index question turns on knowing that.
            FileSplit split = (FileSplit) context.getInputSplit();
            fileName = split.getPath().getName();
        }

        @Override
        public void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {
            StringTokenizer itr = new StringTokenizer(value.toString());
            while (itr.hasMoreTokens()) {
                word.set(itr.nextToken().toLowerCase());
                docId.set(fileName);
                context.write(word, docId);
            }
        }
    }

    public static class IndexReducer
            extends Reducer<Text, Text, Text, Text> {

        private final Text postings = new Text();

        @Override
        public void reduce(Text key, Iterable<Text> values, Context context)
                throws IOException, InterruptedException {
            // Count occurrences per document, in ONE pass over the Iterable.
            Map<String, Integer> freq = new TreeMap<>();
            for (Text doc : values) {
                String d = doc.toString();
                freq.merge(d, 1, Integer::sum);
            }
            StringBuilder sb = new StringBuilder();
            for (Map.Entry<String, Integer> e : freq.entrySet()) {
                if (sb.length() > 0) sb.append(", ");
                sb.append(e.getKey()).append(':').append(e.getValue());
            }
            postings.set(sb.toString());
            context.write(key, postings);
            // The posting list is held in memory here. For a stop word on a
            // real corpus that map does not fit, which is why production
            // indexers emit (term, doc) pairs SORTED and stream the merge --
            // a secondary sort, not a HashMap.
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "inverted index");
        job.setJarByClass(InvertedIndex.class);

        job.setMapperClass(IndexMapper.class);
        job.setReducerClass(IndexReducer.class);
        // NO COMBINER HERE. The reducer's output type (Text postings) differs
        // from its input type (Text docId), and a combiner must have the same
        // input and output types as the reducer. Setting one would not
        // compile -- and if the types happened to match, it would corrupt
        // the counts.

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

// Expected output on the six sample documents (verified in 08_inverted_index.py):
//   dog      doc1.txt:1, doc2.txt:1, doc3.txt:1, doc6.txt:1
//   quick    doc1.txt:1, doc3.txt:2
//   big      doc4.txt:2, doc5.txt:2
//   ... 26 terms, 39 postings
