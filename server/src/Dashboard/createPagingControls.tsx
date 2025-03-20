import type { Accessor } from "solid-js";
import { createSignal } from "solid-js";

export const createPagingControls = (
  totalItems: Accessor<number | undefined>,
  itemsPerPage: Accessor<number>,
  refetch: () => void,
) => {
  const [page, setPage] = createSignal(0);

  const limit = () => itemsPerPage();
  const offset = () => page() * itemsPerPage();
  const numPages = () => Math.ceil((totalItems() ?? 0) / itemsPerPage());

  const enableBack = () => page() > 0;
  const firstPage = () => {
    setPage(0);
    refetch();
  };
  const prevPage = () => {
    setPage((page) => page - 1);
    refetch();
  };

  const enableForward = () => page() < numPages() - 1;
  const nextPage = () => {
    setPage((page) => page + 1);
    refetch();
  };
  const lastPage = () => {
    setPage(numPages() - 1);
    refetch();
  };

  return {
    limit,
    offset,
    page,
    numPages,
    enableBack,
    firstPage,
    prevPage,
    enableForward,
    nextPage,
    lastPage,
  };
};
