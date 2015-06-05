# Post processors

Post processors are meant to enhance and modify the output of a sensor before it is passed on through the nervous system.

The exact same effect can be achieved using commands, but post processors have two main advantages:

- they allow for local processing to occur before going over the wire
- they allow for decentralized, more focused processing depending on minion instance / location

## Examples

### Processing to avoid passing data over the network / latency

Let's think of an example where a minion instance called Dave (whose role is to be the brain) is located at your house, but you installed a simple Minion instance in the office (named "Jerry"), whose job is only to understand a few simple commands such as "Jerry, is it raining at home?" 

You *could* very well grab the spoken audio using for example a SelectiveMicrophoneListener (always on) and send that audio via the nervous system to the brain, then have an STT command grab that audio data and transcribe it; finally a command will process that you asked whether it was raining, and then send back the response.

But that means transferring 100Kb of audio before it can be processed. Post processors allow you to perform the STT process before sending a *text* command over the nervous system (network)

Note that if you use STT such as API.ai or Google Speech API, you are still sending the data over the internet, but you would do that from your other minion instance anyway.

### More accurate processing

Using the same example, you know that you are not going to ask Jerry, the minion in the office, to turn on lights, open the door, or a bunch of other commands that Dave, your minion at home would need to be able to understand.

This means that all the above words - open, door, lights, etc - are not needed as part of Jerry's vocabulary. So if you use a [Pocketsphinx post processor](./audio/pocketsphinx) for example, this would allow you to create a more efficient language model since the vocabulary needed by Jerry is very limited, hence improving the precision of speech to text.

### Security

One of the sensors available in Minion is a [HTTP(s) server](../sensing/http/flask). Depending on your application, it is most likely a good idea to verify that the call to the HTTP server was made from a trusted source. The [Http signature post processor](./http/security#signature) uses a SHA512, salted signature, with timestamp which the application sending making the call to the API will need to match

### Transforming output

As seen in the first example, some post processors transform the type of data, from audio to text for example. You can also transform data without changing its type. For example the [SoX duration limit](./audio/sox#durationlimit) post processor takes in audio data, truncates it to keep only the last 10 seconds - configurable - and outputs audio data again.

Similarly, the [Api.ai text](./text/apiai#command) post processor takes a json encoded string that contains several pieces of information and transforms it to a single command on the corresponding channel
