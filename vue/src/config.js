let BASE_URL = "";

switch (process.env.NODE_ENV) {
  case "development":
    BASE_URL =  process.env.VUE_APP_DATABASE_URL;
    break;
  case "production":
    BASE_URL =  process.env.VUE_APP_DATABASE_URL;
    break
  default:
    break;
}

export default BASE_URL