import { createContext, useContext } from "solid-js";
import type { SetStoreFunction } from "solid-js/store";

interface ComposerStore {
  id: string;
  message: string;
  error: string;
  uploadedFiles: string[];
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
