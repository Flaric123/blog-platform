export const ROLES = Object.freeze({
  ADMIN: Object.freeze({
    NAME: 'admin'
  }),
  AUTHOR: Object.freeze({
    NAME: 'author'
  }),
  READER: Object.freeze({
    NAME: 'reader'
  }),
})
export const GUEST_DATA_DEFAULT = Object.freeze({
  username: undefined,
  role: "non-user",
  api_access_token: undefined,
})