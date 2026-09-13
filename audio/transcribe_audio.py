from basic_pitch.inference import predict


def transcribe_audio(audio_file):
    model_output, midi_data, note_events = predict(
        audio_file,
        onset_threshold=0.5,
        frame_threshold=0.3,
        melodia_trick=False
    )

    print("\nBASIC PITCH NOTES:")
    for event in note_events:
        start_time, end_time, midi_number, amplitude, pitch_bends = event

        print(
            f"{start_time:.3f} - {end_time:.3f} | "
            f"MIDI {midi_number} | "
            f"amplitude {amplitude:.3f}"
        )

    print("TOTAL DETECTED:", len(note_events))

    return note_events