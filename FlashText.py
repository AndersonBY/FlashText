# -*- coding: utf-8 -*-
# @Author: Anderson
# @Date:   2019-04-18 15:53:34
# @Last Modified by:   Anderson
# @Last Modified time: 2019-10-15 13:59:44
print('Importing library. Please wait.')
import librosa
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip
import jieba
import click


@click.command()
@click.option('--width', prompt='Width', default=360, help='The width of video clips')
@click.option('--height', prompt='Height', default=240, help='The height of video clips')
@click.option('--text', prompt='Text file', default='text.txt', help='The source text file')
@click.option('--music', prompt='Music file', default='改革春风吹满地.mp3', help='The music file')
@click.option('--word_split', prompt='Split words', default=False, help='Split words or not')
@click.option('--output', prompt='Output file', default='FlashText.mp4', help='The output file name')
def main(width, height, text, music, word_split, output):
	with open(text, 'r', encoding='utf-8') as f:
		text_str = f.read()
	if word_split:
		seg_list = jieba.lcut(text_str)
		punct = set(''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
		﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
		々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
		︽︿﹁﹃﹙﹛﹝（｛“‘-—_…/\\''')
		word_list = list(filter(lambda x: x not in punct, seg_list))
	else:
		word_list = text_str.split('\n')

	y, sr = librosa.load(music)
	tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
	beat_times = list(librosa.frames_to_time(beats, sr=sr))
	beat_times.append(beat_times[-1] + 1)

	clips = []
	for index, beat_time in enumerate(beat_times[:-1]):
		if index >= len(word_list):
			break
		print(f'{index + 1}/{len(beat_times)}——{word_list[index]}')
		text_clip = TextClip(
			word_list[index],
			fontsize=width // 8,
			color='white',
			size=(width, height),
			method='caption',
			font='msyhbd.ttc')\
			.set_start(beat_time)\
			.set_end(beat_times[index + 1])
		text_clip = text_clip.set_pos('center')
		clips.append(text_clip)

	final_clip = CompositeVideoClip(clips)
	audio_clip = AudioFileClip(music)
	final_video = final_clip.set_audio(audio_clip)
	final_video.write_videofile(
		output,
		fps=30,
		codec='mpeg4',
		preset='ultrafast',
		audio_codec="libmp3lame",
		threads=4)


if __name__ == '__main__':
	main()
