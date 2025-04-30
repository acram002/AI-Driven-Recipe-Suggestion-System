import api from "@/api";

export const isAuthenticated = async () => {
  try {
    await api.get("/user/profile/"); // This will succeed if the user is logged in
    return true;
  } catch (error) {
    return false; // API call fails if user is not authenticated
  }
};
