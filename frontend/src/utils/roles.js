// src/utils/roles.js

export function normalizeRoles(roles = []) {
  return roles.map((r) =>
    typeof r === "string"
      ? r.toLowerCase()
      : r.name.toLowerCase()
  );
}
