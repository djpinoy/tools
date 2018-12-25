for f in *.MP4
do
	basename=$(echo "$f" | cut -f 1 -d '.')
	echo $basename
	
	mp4_name=$basename
	mp4_name+=.MP4
	wav_name=$basename
	wav_name+=.WAV
	merge_name=merge_
	merge_name+=$basename
	merge_name+=.MP4

	echo $mp4_name
	echo $wav_name
	echo $merge_name

	ffmpeg -i $mp4_name -i $wav_name -af dynaudnorm=m=35 -map 0:0 -map 1:0 -c:v copy -c:a aac -b:a 256k -shortest $merge_name
done
