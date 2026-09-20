import os
from openai import OpenAI
import streamlit as st
from comparison.compare_notes import CORRECT
from comparison.compare_timing import ON_TIME
from .prompts import AI_PROMPT
from comparison.measure_summary import build_measure_summary, score_staff_label


api_key = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)


def generate_feedback(report, language="English"):
    measure_summary = build_measure_summary(report)

    prompt = []

    prompt.append("Comparison Results")
    prompt.append("")

    prompt.append("Overall Results:")
    prompt.append(str(report.overall_result))
    prompt.append("")

    prompt.append("Measure-by-Measure Results:")
    prompt.append(str(measure_summary))
    prompt.append("")

    prompt.append("Important interpretation rule:")
    prompt.append("Treat the comparison results as evidence, not as proof of player intent.")
    prompt.append(
        "Do not describe a played note as a substitution for an expected note "
        "unless the data clearly supports that conclusion."
    )
    prompt.append("Do not invent mistakes or patterns that are not present in the data.")
    prompt.append("")

    prompt.append("Specific Note-Level Evidence:")

    for (expected, played), note_result, timing_result in zip(report.aligned_notes,report.note_results,report.timing_results):

        if note_result == CORRECT and timing_result.result == ON_TIME:
            continue

        if expected is not None:
            expected_note = f"{expected.pitch}{expected.octave}"
            measure = expected.measure
            beat = expected.beat
            staff = score_staff_label(expected.staff)
        else:
            expected_note = "No note expected"
            measure = "extra"
            beat = played.beat if played is not None else "unknown"
            staff = None

        if played is not None:
            played_note = f"{played.pitch}{played.octave}"
        else:
            played_note = "No note played"

        location = f"- Measure {measure}, beat {beat}"
        if staff is not None:
            location += f", {staff}"

        prompt.append(f"{location}: Expected {expected_note}, Played {played_note}")

        if note_result != CORRECT:
            prompt.append(f"  Pitch result: {note_result}")

        if timing_result.result != ON_TIME:
            prompt.append(f"  Timing result: {timing_result.result}")

    prompt.append("")
    prompt.append(f"Write the final feedback in {language}.")
    prompt.append("Keep the language natural and easy for a piano student to understand.")
    prompt.append("Do not translate or change the underlying performance results.")

    user_prompt = "\n".join(prompt)

    response = client.responses.create(
        model="gpt-5",
        input=[{"role": "system","content": AI_PROMPT},{"role": "user","content": user_prompt}]
    )

    return response.output_text

