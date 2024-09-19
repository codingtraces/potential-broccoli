To create a structured Word document that mimics a letter-like format using a FAP-like file, we will need to refine the approach to include multiple paragraphs and an image (e.g., a logo). The idea is to structure the FAP content in a way that clearly separates different elements, such as paragraphs and images, while maintaining the correct order and formatting in the final Word document.

### Step 1: Sample FAP File with Two Paragraphs and a Logo

Let's create a sample FAP file that contains two paragraphs of text and a logo. We will simulate a basic structure to avoid client information while retaining the essence of the format:

```plaintext
H,2400,(0,0),(0,0,26400,20400),SampleLetterFAP
V,"A123456X","JOHN","Mon Jan 01 10:00:00 2022",".","."
V,"B654321X","DOE","Mon Jan 01 10:15:00 2022",".","."
M,TT,(18952,4460,19296,5364),(20011,Bold,14),1,Dear John Doe,
M,TT,(18952,5386,19296,6418),(20011,Regular,12),2,We are pleased to inform you that your application has been approved.
M,TT,(18952,6440,19296,6940),(20011,Regular,12),3,Please find the details below regarding your approval and next steps.
M,TT,(18952,7500,19296,8000),(20011,Regular,12),4,Your contract will commence on February 1, 2022.
M,O,(19384,9432,19728,9432),(20011,Regular,100),5,logo.png
M,TT,(18952,8500,19296,9000),(20011,Regular,12),6,If you have any questions, please contact our support team.
M,TT,(18952,9500,19296,10000),(20011,Bold,14),7,Thank you,
M,TT,(18952,10500,19296,11000),(20011,Bold,14),8,Your Company Name
M,E
```

### Step 2: Modify the `FapParser` Class

The `FapParser` class needs to handle both text and image elements, including their respective details:

```java
package com.example.fapwordconverter;

import java.util.ArrayList;
import java.util.List;

public class FapParser {

    public List<FapElement> parseFapFile(String fileContent) {
        List<FapElement> elements = new ArrayList<>();

        String[] lines = fileContent.split("\n");
        for (String line : lines) {
            if (line.startsWith("M,TT")) {
                elements.add(parseTextElement(line));
            } else if (line.startsWith("M,O")) {
                elements.add(parseImageElement(line));
            }
        }

        return elements;
    }

    private FapElement parseTextElement(String line) {
        String[] parts = line.split(",", 7); // Split into 7 parts
        String coordinates = parts[2];
        String fontDetails = parts[3];
        int fontSize = Integer.parseInt(parts[4].trim());
        String content = parts[6].trim();

        return new FapElement("TEXT", content, coordinates, fontDetails, fontSize);
    }

    private FapElement parseImageElement(String line) {
        String[] parts = line.split(",", 6); // Split into 6 parts
        String coordinates = parts[2];
        String fontDetails = parts[3];
        String imagePath = parts[5].trim();

        return new FapElement("IMAGE", imagePath, coordinates, fontDetails, 0);
    }

    public static class FapElement {
        private String type;
        private String content;
        private String coordinates;
        private String fontDetails;
        private int fontSize;

        public FapElement(String type, String content, String coordinates, String fontDetails, int fontSize) {
            this.type = type;
            this.content = content;
            this.coordinates = coordinates;
            this.fontDetails = fontDetails;
            this.fontSize = fontSize;
        }

        public String getType() {
            return type;
        }

        public String getContent() {
            return content;
        }

        public String getCoordinates() {
            return coordinates;
        }

        public String getFontDetails() {
            return fontDetails;
        }

        public int getFontSize() {
            return fontSize;
        }
    }
}
```

### Step 3: Enhance the `WordGenerator` Class

This class will need to handle both text and image elements, applying the appropriate styling and adding the logo image to the document.

```java
package com.example.fapwordconverter;

import org.apache.poi.xwpf.usermodel.*;
import org.apache.poi.util.Units;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Path;
import java.util.List;

public class WordGenerator {

    public void generateWordDocument(List<FapParser.FapElement> elements, Path outputPath) throws IOException {
        try (XWPFDocument doc = new XWPFDocument()) {
            for (FapParser.FapElement element : elements) {
                if (element.getType().equals("TEXT")) {
                    addText(doc, element);
                } else if (element.getType().equals("IMAGE")) {
                    addImage(doc, element);
                }
            }

            try (FileOutputStream out = new FileOutputStream(outputPath.toFile())) {
                doc.write(out);
            }
        }
    }

    private void addText(XWPFDocument doc, FapParser.FapElement element) {
        XWPFParagraph paragraph = doc.createParagraph();
        paragraph.setAlignment(ParagraphAlignment.LEFT);

        XWPFRun run = paragraph.createRun();
        run.setText(element.getContent());
        run.setFontSize(getFontSize(element.getFontSize()));
        setFontStyle(run, element.getFontDetails());
    }

    private int getFontSize(int fapFontSize) {
        return Math.max(fapFontSize / 2, 10);  // Convert to a reasonable point size
    }

    private void setFontStyle(XWPFRun run, String fontDetails) {
        if (fontDetails.contains("Bold")) {
            run.setBold(true);
        }
        if (fontDetails.contains("Italic")) {
            run.setItalic(true);
        }
    }

    private void addImage(XWPFDocument doc, FapParser.FapElement element) throws IOException {
        XWPFParagraph paragraph = doc.createParagraph();
        XWPFRun run = paragraph.createRun();

        try (FileInputStream is = new FileInputStream(element.getContent())) {
            run.addPicture(is, Document.PICTURE_TYPE_PNG, element.getContent(), Units.toEMU(100), Units.toEMU(50)); // Adjust size as needed
        }
    }
}
```

### Step 4: Main Application (`Main.java`)

The main application remains largely unchanged but ensures that it correctly processes both text and image elements.

```java
package com.example.fapwordconverter;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

public class Main {

    public static void main(String[] args) {
        try {
            Path inputPath = Paths.get("input/sample.fap");
            Path outputPath = Paths.get("output/sample.docx");

            Files.createDirectories(outputPath.getParent());

            String content = Files.readString(inputPath);

            FapParser fapParser = new FapParser();
            List<FapParser.FapElement> elements = fapParser.parseFapFile(content);

            WordGenerator wordGenerator = new WordGenerator();
            wordGenerator.generateWordDocument(elements, outputPath);

            System.out.println("Word document generated successfully at: " + outputPath);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

### Step 5: Prepare the Environment

1. **Create Directories**:
   - Ensure you have an `input` directory in the project root.
   - Ensure you have an `output` directory in the project root.

2. **Add `sample.fap`**:
   - Place the `sample.fap` file inside the `input` directory.

3. **Add an Image**:
   - Place an image file named `logo.png` inside the `input` directory or any other accessible location. Ensure the `sample.fap` file references this path correctly.

### Step 6: Run the Application

1. **Build the Project**:
   - Use **Build > Build Project** in IntelliJ IDEA.

2. **Run the Application**:
   - Run `Main.java` as a Java application.

3. **Check Output**:
   - A new `sample.docx` should be generated in the `output` directory. Open it to verify that it contains the formatted paragraphs and the logo.

### Expected Output

- **Two Paragraphs**:
  - The Word document should have two paragraphs, with appropriate text formatting (e.g., bold, regular).
- **Logo**:
  - The document should include the logo image at the specified position.

### Troubleshooting and Notes:

- **Font and Position**: Apache POI doesn't fully support absolute positioning as in GUI tools like Documaker, so position elements as closely as possible using paragraphs and alignments.
- **Images**: Ensure your images are correctly referenced and exist at the specified location. Adjust image sizes as necessary.
- **Scaling**: For complex documents,

 consider adding more advanced formatting rules or integrating this with a more comprehensive document creation tool.

This setup provides a basic structure for converting FAP-like content into a Word document while respecting text formatting and including images like logos.
