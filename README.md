# extract_naomi_corpus

This is a simple file for extracting a corpus from Naomi for training a language model. The idea is that the intents for the different speechhandler plugins contain all the ways in which the user can activate a plugin, so can be used to generate a model of all expected utterances.

This is very experimental and meant to be used with Mozilla STT to create language models that contain word sequences rather than individual words.

Right now I am just pulling the raw templates and deleting any placeholders. This should work well enough for an experiment since right now Naomi has very few templates that actually use keywords, but will definitely need to be improved by adding a line for every possible option in a keyword situation, and also including some indicator (<UNK>?) for unknown words.

In the case of unknowns, it would be cool to either be able to feed the audio to a more general language model along with the partial translation, or identify exactly where the temporal boundaries of the unknown word are in the audio file and clip that little part and feed it to a general language model.
