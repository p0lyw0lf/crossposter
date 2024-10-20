/**
 * Returns the resulting file URLs
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
