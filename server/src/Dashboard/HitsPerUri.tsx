import type { Component } from "solid-js";
import { HitsPerStringKey } from "./HitsPerStringKey";

export const HitsPerUri: Component = () => {
  // TODO: I may eventually want to break this down by folder? prob not tho lol
  return <HitsPerStringKey colName="cs-uri-stem" keyName="URI" hasPaging />;
};
