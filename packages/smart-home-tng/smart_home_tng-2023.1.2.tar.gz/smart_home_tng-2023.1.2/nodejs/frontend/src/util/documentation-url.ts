import { HomeAssistant } from "../types";

export const documentationUrl = (hass: HomeAssistant, path: string) =>
  `https://${
    hass.config.version.includes("b")
      ? "rc"
      : hass.config.version.includes("dev")
      ? "next"
      : "www"
  }.home-assistant.io${path}`;

export const githubUrl = (path: string) =>
  `https://github.com/nixe64/the-next-generation${path}`;