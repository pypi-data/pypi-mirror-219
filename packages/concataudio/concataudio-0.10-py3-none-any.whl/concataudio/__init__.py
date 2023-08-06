from pydub import AudioSegment


def read_audio_file(filename):
    """
    Read an audio file and extract its properties.

    Parameters:
        filename (str): The path to the audio file.

    Returns:
        tuple: A tuple containing:
            - audio_data (AudioSegment): The audio data loaded from the file.
            - num_channels (int): The number of audio channels (1 for mono, 2 for stereo).
            - sample_width (int): The sample width in bytes (e.g., 1 for 8-bit, 2 for 16-bit).
            - frame_rate (int): The frame rate in Hz (number of audio frames per second).
    """
    audio_data = AudioSegment.from_file(filename)
    num_channels = audio_data.channels
    sample_width = audio_data.sample_width
    frame_rate = audio_data.frame_rate

    return audio_data, num_channels, sample_width, frame_rate


def resample_audio(audio_data, frame_rate, target_frame_rate):
    """
    Resample the audio data to a target frame rate.

    Parameters:
        audio_data (AudioSegment): The audio data to be resampled.
        frame_rate (int): The original frame rate of the audio data.
        target_frame_rate (int): The desired frame rate to resample the audio data to.

    Returns:
        AudioSegment: The resampled audio data.
    """
    audio = audio_data.set_frame_rate(target_frame_rate)
    return audio


def convert_sample_width(audio_data, sample_width, target_sample_width):
    """
    Convert the audio data's sample width to a target sample width.

    Parameters:
        audio_data (AudioSegment): The audio data to be converted.
        sample_width (int): The original sample width in bytes.
        target_sample_width (int): The desired sample width to convert the audio data to.

    Returns:
        AudioSegment: The audio data with the new sample width.
    """
    audio = audio_data.set_sample_width(target_sample_width)
    return audio


def concatenate_audio(audio_data1, audio_data2):
    """
    Concatenate two audio data segments.

    Parameters:
        audio_data1 (AudioSegment): The first audio data segment.
        audio_data2 (AudioSegment): The second audio data segment.

    Returns:
        AudioSegment: The concatenated audio data.
    """
    combined_audio = audio_data1 + audio_data2
    return combined_audio


def concat_audio_files(audio_file_list, output_file, file_format="wav"):
    r"""
    Concatenate multiple audio files from the given list and export the result.

    Parameters:
        audio_file_list (list): A list of file paths for the audio files to be concatenated.
        output_file (str): The path to save the output concatenated audio file.
        file_format (str, optional): The format of the output file. Defaults to 'wav'.

    Example:
        from concataudio import concat_audio_files
        audio_file_list = [r"C:\welcheantwort.wav", r"C:\ProgramData\anaconda3\envs\soundtest\speech_orig.wav",
                           r"C:\welcheantwort.wav"]
        concat_audio_files(audio_file_list, output_file='c:\\output_audio3.wav', file_format='wav')
    """
    audio_data1, num_channels1, sample_width1, frame_rate1 = read_audio_file(
        audio_file_list[0]
    )
    combined_audio = audio_data1

    for audiofile in audio_file_list[1:]:
        audio_data2, num_channels2, sample_width2, frame_rate2 = read_audio_file(
            audiofile
        )

        # Resample audio_data2 to match frame_rate1
        if frame_rate1 != frame_rate2:
            audio_data2 = resample_audio(audio_data2, frame_rate2, frame_rate1)

        # Convert sample_width2 to match sample_width1
        if sample_width1 != sample_width2:
            audio_data2 = convert_sample_width(
                audio_data2, sample_width2, sample_width1
            )

        combined_audio += audio_data2

    # Concatenate the audio data and export it
    combined_audio.export(output_file, format=file_format)
