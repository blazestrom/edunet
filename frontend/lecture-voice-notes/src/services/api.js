import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

export async function uploadAudio(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(`${BASE_URL}/api/process`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
}
