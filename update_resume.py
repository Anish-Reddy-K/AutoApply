import os
import subprocess

def update_resume(latex_file_path, bullet_points_file, output_pdf_path):
    # Read the bullet points from the text file
    with open(bullet_points_file, 'r') as file:
        bullet_points = file.readlines()
    
    # Ensure we have exactly 8 lines (4 for each job)
    if len(bullet_points) < 8:
        raise ValueError("The bullet points file must contain at least 8 lines.")
    
    # Prepare the replacements for LaTeX
    replacements = {
        '%JOB1_POINT1%': bullet_points[0].strip(),
        '%JOB1_POINT2%': bullet_points[1].strip(),
        '%JOB1_POINT3%': bullet_points[2].strip(),
        '%JOB1_POINT4%': bullet_points[3].strip(),
        '%JOB2_POINT1%': bullet_points[4].strip(),
        '%JOB2_POINT2%': bullet_points[5].strip(),
        '%JOB2_POINT3%': bullet_points[6].strip(),
        '%JOB2_POINT4%': bullet_points[7].strip(),
    }

    # Read the LaTeX resume template
    with open(latex_file_path, 'r') as file:
        latex_content = file.read()
    
    # Replace the placeholders with the bullet points
    for placeholder, bullet_point in replacements.items():
        latex_content = latex_content.replace(placeholder, bullet_point)
    
    # Save the modified LaTeX content to a new file
    updated_latex_file = 'updated_resume.tex'
    with open(updated_latex_file, 'w') as file:
        file.write(latex_content)

    # Compile the LaTeX file to a PDF
    try:
        subprocess.run(['pdflatex', updated_latex_file], check=True)
        # Move the generated PDF to the desired output path
        if os.path.exists(output_pdf_path):
            os.remove(output_pdf_path)
        os.rename('updated_resume.pdf', output_pdf_path)
    except subprocess.CalledProcessError as e:
        print(f"Error during LaTeX compilation: {e}")
        return False

    # Clean up auxiliary files generated during compilation
    for ext in ['aux', 'log', 'out', 'tex']:
        aux_file = f'updated_resume.{ext}'
        if os.path.exists(aux_file):
            os.remove(aux_file)

    return True

# Example usage
latex_file_path = 'resume_template.tex'  # Path to your LaTeX resume file
bullet_points_file = 'points.txt'  # Path to the file with the bullet points
output_pdf_path = 'D:\Code\AutoApply'  # Output PDF file path

if update_resume(latex_file_path, bullet_points_file, output_pdf_path):
    print(f"Resume updated successfully. Saved as {output_pdf_path}")
else:
    print("Failed to update resume.")
