import axios from "axios";

const instance = axios.create({
  baseURL: "http://localhost:8000/api",
});

instance.interceptors.response.use((response) => {
  console.log(this);
  if(response.data.error)
    throw response.data.error;
  return response
}, (error) => {
  return Promise.reject(error)
})

export default instance;