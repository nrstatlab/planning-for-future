// Experiment 18 -- GridFS: storing and retrieving large files.
//
// *** NOT EXECUTED ***
// mongomock does not implement GridFS, and mongod cannot be installed in the
// verification environment (the Debian repositories that host mongodb-org are
// blocked by the egress policy). So this file has never been run here and has
// NO .py half. The chunk arithmetic below is arithmetic, not a measurement.
// See notes/sem-4/course-10-document-database/lab.md.

// =============================================================================
// WHY GridFS EXISTS
// =============================================================================
// A BSON document is capped at 16 MB. GridFS gets round that by splitting the
// file into chunks of 255 KB and storing each chunk as its own document.
//
//   fs.files   -- ONE metadata document per file
//   fs.chunks  -- MANY documents, each a 255 KB slice, with files_id and n
//
// The 16 MB cap is not arbitrary: it is what keeps a single document cheap to
// move around in memory and over the wire. GridFS does not remove the cap; it
// works within it.

// =============================================================================
// 1. From the command line: mongofiles
// =============================================================================
//   mongofiles -d collegeDB put lecture.mp4
//   mongofiles -d collegeDB list
//   mongofiles -d collegeDB get lecture.mp4
//   mongofiles -d collegeDB delete lecture.mp4
//   mongofiles -d collegeDB --local ./copy.mp4 get lecture.mp4
//
// mongofiles ships with the MongoDB Database Tools, a SEPARATE download from
// the server. That trips people up.

// =============================================================================
// 2. Looking at what it stored
// =============================================================================
use collegeDB
db.fs.files.find().pretty()
// { _id, length, chunkSize: 261120, uploadDate, filename, metadata }

db.fs.chunks.find({}, { data: 0 }).sort({ n: 1 }).limit(3)
// { _id, files_id, n: 0 }, { ..., n: 1 }, ...   -- n is the ORDER

db.fs.chunks.countDocuments({ files_id: <the _id from fs.files> })

// --- THE ARITHMETIC, which is what gets asked ---------------------------------
// chunkSize is 255 KB = 255 * 1024 = 261120 bytes.
//
//   chunks = ceil(length / 261120)
//
//   1 MB     =  1048576 B -> ceil(1048576/261120)  =     5 chunks
//   10 MB    = 10485760 B -> ceil(10485760/261120) =    41 chunks
//   100 MB   = 104857600  -> ceil(104857600/261120)=   402 chunks
//   1 GB     = 1073741824 -> ceil(1073741824/261120)=  4113 chunks
//
// The LAST chunk is short -- GridFS does not pad. So the stored size is the
// file's size plus a little metadata, not a multiple of 255 KB.

// --- the indexes GridFS creates for itself -----------------------------------
db.fs.chunks.getIndexes()      // { files_id: 1, n: 1 }, UNIQUE
db.fs.files.getIndexes()       // { filename: 1, uploadDate: 1 }
// The unique compound index on (files_id, n) is what guarantees the chunks
// reassemble in the right order and cannot be duplicated.

// =============================================================================
// 3. From the shell / a driver
// =============================================================================
// mongosh has no built-in put; you use a driver. In Node:
//
//   const bucket = new GridFSBucket(db, { bucketName: "lectures" });
//   fs.createReadStream("lecture.mp4").pipe(bucket.openUploadStream("lecture.mp4",
//       { metadata: { course: "DSC301", week: 3 } }));
//   bucket.openDownloadStreamByName("lecture.mp4").pipe(res);
//
// A custom bucketName gives lectures.files / lectures.chunks instead of fs.*.
//
// STREAMING IS THE POINT. openDownloadStream can start at any byte:
//   bucket.openDownloadStreamByName("lecture.mp4", { start: 5_000_000 })
// which is how a video seeks without downloading the whole file first.

// =============================================================================
// 4. Querying by metadata -- what a filesystem cannot do
// =============================================================================
db.fs.files.find({ "metadata.course": "DSC301" })
db.fs.files.find({ length: { $gt: 50 * 1024 * 1024 } })
db.fs.files.aggregate([
  { $group: { _id: "$metadata.course", n: { $sum: 1 },
              totalBytes: { $sum: "$length" } } }
])
db.fs.files.createIndex({ "metadata.course": 1, uploadDate: -1 })

// =============================================================================
// 5. Deleting -- the one thing to be careful about
// =============================================================================
// WRONG: this orphans every chunk of the file.
//   db.fs.files.deleteOne({ filename: "lecture.mp4" })
//
// RIGHT: use the driver's bucket.delete(id) or mongofiles delete, which
// removes the metadata document AND its chunks. GridFS is two collections
// kept consistent by the DRIVER, not by the database -- there is no cascade.

// =============================================================================
// WHEN NOT TO USE GridFS -- worth a mark, and usually the right answer
// =============================================================================
// USE IT when:
//   * files exceed 16 MB
//   * you need RANGE reads (video seeking)
//   * you want the file and its metadata under one backup and one replica set
//   * atomic-ish updates matter more than throughput
//
// DO NOT use it when:
//   * files are small and numerous -- the chunk documents cost more than they
//     save, and a plain BinData field under 16 MB is simpler
//   * you are serving them over HTTP at volume -- S3 or a CDN is faster,
//     cheaper, and does not put the read load on your database
//
// The honest summary: GridFS is a good answer when the files must live with
// the data. It is rarely the best answer for a website's static assets.
