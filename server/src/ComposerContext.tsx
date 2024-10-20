import { createContext, useContext } from "solid-js";
import type { Draft } from "./drafts";
import type { SetStoreFunction } from "solid-js/store";

interface ComposerStore {
  formRef: HTMLFormElement;
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
      "useComposerContext must be used inside a ComposerProvider"
    );
  }
  return context;
};

export const ComposerProvider = ComposerContext.Provider;
