This example shows a very simple example of how to parse a small CSV file.

The well-known iris dataset is used.

The H2O examples use the h2o.uploadFile method, which is a "push-to-h2o" operation.

This is not scalable, and only intended for smaller data sizes.  The client pushes the data from a local filesystem (for example on your laptop where R is running) to H2O.

For big-data operations, you don't want the data stored on, or flowing through, the client.
