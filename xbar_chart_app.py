import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="X̄ Chart from Question", layout="wide")
st.title("🧠 X̄ (X-bar) Chart from Natural Language with Smart Feedback")

st.markdown("### Step 1: Type a question with sample measurements")
st.code("Example: I collected 3 samples: 10.2, 10.5, 10.1, 10.3, 10.4; 9.9, 10.1, 9.8, 10.0, 9.9; and 10.5, 10.6, 10.4, 10.7, 10.5.")

question = st.text_area("Enter your question here:")

if st.button("Generate Chart and Analyze") and question:
    try:
        # Extract sets of numbers
        pattern = r'((?:\d+(?:\.\d+)?,\s*){4,}\d+(?:\.\d+)?)'
        matches = re.findall(pattern, question)

        if not matches:
            st.warning("Could not find valid data in your question. Please try again.")
        else:
            samples = [list(map(float, m.strip().split(','))) for m in matches]
            sample_means = [np.mean(sample) for sample in samples]
            sample_ranges = [np.max(sample) - np.min(sample) for sample in samples]

            X_bar = np.mean(sample_means)
            R_bar = np.mean(sample_ranges)
            n = len(samples[0]) if samples else 5

            A2_dict = {2: 1.880, 3: 1.023, 4: 0.729, 5: 0.577, 6: 0.483, 7: 0.419, 8: 0.373, 9: 0.337, 10: 0.308}
            A2 = A2_dict.get(n, 0.577)

            UCL = X_bar + A2 * R_bar
            LCL = X_bar - A2 * R_bar

            st.success(f"CL = {X_bar:.2f}, UCL = {UCL:.2f}, LCL = {LCL:.2f}")

            # Check process control status
            out_of_control = [i+1 for i, mean in enumerate(sample_means) if mean < LCL or mean > UCL]

            # Auto explanation
            if out_of_control:
                st.error(f"❌ The process is **out of control** at sample(s): {', '.join(map(str, out_of_control))}.")
            else:
                st.success("✅ The process is **in control**. All sample means are within control limits.")

            # Plot the chart
            fig, ax = plt.subplots()
            ax.plot(range(1, len(sample_means) + 1), sample_means, marker='o', label='Sample Means')
            ax.axhline(X_bar, color='green', linestyle='--', label='CL')
            ax.axhline(UCL, color='red', linestyle='--', label='UCL')
            ax.axhline(LCL, color='red', linestyle='--', label='LCL')
            ax.set_xlabel('Sample Number')
            ax.set_ylabel('Sample Mean')
            ax.set_title('X̄ Control Chart')
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
