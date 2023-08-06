# Concatenates multiple audio files from the given list and exports the result.

## pip install concataudio 

#### Tested against Windows 10 / Python 3.10 / Anaconda 



```python
Concatenates multiple audio files from the given list and exports the result.

Parameters:
	audio_file_list (list): A list of file paths for the audio files to be concatenated.
	output_file (str): The path to save the output concatenated audio file.
	file_format (str, optional): The format of the output file. Defaults to 'wav'.

Example:
	from concataudio import concat_audio_files
	audio_file_list = [r"C:\welcheantwort.wav", r"C:\ProgramData\anaconda3\envs\soundtest\speech_orig.wav",
					   r"C:\welcheantwort.wav"]
	concat_audio_files(audio_file_list, output_file='c:\\output_audio3.wav', file_format='wav')

```