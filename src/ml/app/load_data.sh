#!/bin/bash
curl -o ./model.zip https://alphacephei.com/vosk/models/vosk-model-ru-0.22.zip
unzip model.zip
mv vosk-model-ru-0.22/ model
rm -rf model.zip