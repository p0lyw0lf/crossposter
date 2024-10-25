import { getFormElements } from "./ComposerContext";
import { resizeTextArea } from "./components/TextArea";

/**
 * Returns the uploaded file URLs
 */
export const uploadFiles = async (
  id: string,
  files: File[]
): Promise<string[]> => {
  return await Promise.all(
    files.map(async (file) => {
      const url = new URL("/upload", window.location.origin);
      url.searchParams.set("f", `blog/${id}/${file.name}`);
      const response = await fetch(url, { method: "POST", body: file });
      if (!response.ok) {
        throw new Error(`server response ${response.status}`);
      }
      return await response.text();
    })
  );
};

/**
 * Uploads files and inserts the resulting urls as Markdown image links into
 * the form's body text.
 *
 * Returns the uploaded file URLs
 */
export const uploadFilesAndInsert = async (
  formRef: HTMLFormElement,
  files: File[]
): Promise<string[]> => {
  const id = getFormElements(formRef).draftId.value;
  const filenames = await uploadFiles(id, files);

  const { body } = getFormElements(formRef);
  body.setRangeText(
    filenames.map((filename) => `![](${filename})`).join("\n\n")
  );
  resizeTextArea(body);

  return filenames;
};
