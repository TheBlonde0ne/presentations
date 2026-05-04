### The HTML/Reveal.js Super-Prompt

**Role:** You are a Full-Stack Developer and an Expert Physicist. Your goal is to create a complete, self-contained HTML file for a `reveal.js` presentation based on the uploaded research papers.

**Context:** This is Topic 8 of an Altermagnetism seminar: "Probing Magnetism with Light." Topics 1–7 (Symmetry, ARPES, etc.) have already been covered. My talk focuses on the dielectric tensor, MOKKA, and experimental optical evidence.

**Technical Requirements:**
1.  **Output Format:** Provide one single, valid HTML file. 
2.  **Dependencies:** Use `reveal.js` and `MathJax` (for LaTeX) via CDN links so the file runs immediately in a browser.
3.  **Styling:** 
    *   Incorporate the logic and aesthetic from my uploaded `styles.css` file into the `<style>` block.
    *   Ensure slides use a clean, dark-themed academic layout.
    *   Use `flexbox` or `grid` for slides that compare two figures (e.g., $\kappa$-Cl vs. $RuO_2$).
4.  **Physics Content:**
    *   **Slide 1 (Title):** Title, My Name, Seminar Series Info.
    *   **Slide 2 (Context):** Briefly bridge from Topic 4 (ARPES) to Topic 8 (Bulk Optics).
    *   **Slide 3 (The Dielectric Tensor):** Mathematical breakdown of $\varepsilon_{ij}$ and why $\sigma_{xy}$ is the "smoking gun."
    *   **Slide 4-5 (MOKKA):** Detailed explanation of the Kramers-Kronig analysis and the "45-degree fast protocol." Include the relevant integral equations in LaTeX.
    *   **Slide 6-7 (The Organic Success):** Focus on $\kappa$-Cl, the non-linear field dependence, and the 100 meV splitting vs. 1 meV SOC argument.
    *   **Slide 8-9 (The RuO2 Controversy):** Present the Pauli Edge and Plasma Frequency data. Contrast why this contradicts the altermagnetic theory.
    *   **Slide 10 (Phonon CD):** Explain the $Co_3Sn_2S_2$ case and the Fano lineshape formula.
    *   **Slide 11 (Summary/Q&A):** A table comparing the "Optical Evidence Strength" of the discussed materials.

**Instructions for Slide Content:**
*   **Don't be brief.** Each slide should have a clear heading, 3-5 high-level technical bullet points, and a footer or sidebar for the specific paper citation (e.g., "Wenzel et al., 2024").
*   **Speaker Notes:** Use the `<aside class="notes">` tag for every slide to provide a 200-word deep-dive script that I can read while presenting.

---

### How to execute this for maximum effectiveness:

1.  **Upload the Files:** In Google AI Studio, click the `+` and upload:
    *   The 5 PDF papers.
    *   Your `styles.css`.
2.  **Model Settings:** Use **Gemini 1.5 Pro**. Set the **Output Length** slider to the maximum (usually 8192 or higher) because a 45-minute slide deck with speaker notes is a very long text output.
3.  **Check the LaTeX:** Reveal.js handles LaTeX through MathJax. Ensure the prompt includes:
    *   `$$ ... $$` for display equations.
    *   `$ ... $` for inline math.
4.  **Handling "Cut-offs":** If the AI stops generating code mid-way (a common issue with long HTML files), simply type: **"You cut off at [Last Line of Code]. Please continue the HTML code exactly from there to the end."**
