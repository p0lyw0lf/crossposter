import { createContext, useContext } from "solid-js";
import type { SetStoreFunction } from "solid-js/store";
import type { Draft } from "./drafts";

interface ComposerStore {
  formRef: HTMLFormElement;
  preview: boolean;
  message: string;
  error: string;
  tags: string[];
  drafts: Draft[];
}

interface Context {
  store: ComposerStore;
  setStore: SetStoreFunction<ComposerStore>;
}

const ComposerContext = createContext<Context>();

export const useComposerContext = (): Context => {
  const context = useContext(ComposerContext);
  if (context === undefined) {
    throw new Error(
      "useComposerContext must be used inside a ComposerProvider",
    );
  }
  return context;
};

export const ComposerProvider = ComposerContext.Provider;

interface FormElements {
  draftId: HTMLInputElement;
  body: HTMLTextAreaElement;
  title: HTMLTextAreaElement;
}

export const getFormElements = (formRef: HTMLFormElement): FormElements => {
  // SAFETY: this is how the form is laid out
  return formRef.elements as any;
};
