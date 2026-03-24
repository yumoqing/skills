#!/usr/bin/env bash
## 需要从标准输入获得参数
skilldir=$(pwd)
mkdir -p tmp
cd tmp
cdir=$(pwd)
id=tmp$$
adir=${cdir}/${id}/separated/htdemucs/output_audio${id}
echo $id
ffmpeg -i $1 -c:v copy -an output_video${id}.mp4 -c:a pcm_s16le -f wav output_a
udio${id}.wav
echo ls -l output_video*
ls -l output_video*
mkdir ${id}
cd ${id}
${skilldir}/py3/bin/demucs --two-stems=vocals ${cdir}/output_audio${id}.wav
echo ls -l ${adir}
ls -l ${adir}
cd ${cdir}
ffmpeg -i output_video${id}.mp4 -i ${adir}/no_vocals.wav -i ${adir}/vocals.wav 
\
    -map 0:v:0 \
    -map 1:a:0 \
    -map 2:a:0 \
    -c:v copy \
    -c:a aac -b:a 192k \
    -metadata:s:a:0 title="伴奏" \
    -metadata:s:a:1 title="原唱" \
    output_ktv.mkv -y
# rm -rf ${id} output_video${id}.mp4 output_audio${id}.wav
echo ls ${cdir}/output_ktv.mkv
ls ${cdir}/output_ktv.mkv
echo ${cdir}/output_ktv.mkv

