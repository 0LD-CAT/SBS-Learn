import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { getUserProfile } from "../api/user";


export default function OAuthSuccess() {
  const navigate = useNavigate();

  useEffect(() => {
    const params =
      new URLSearchParams(window.location.search);
    const token =
      params.get("token");

    const handleOAuth = async () => {
      if (!token)
        return;

      localStorage.setItem(
        "token",
        token
      );

      const profile =
        await getUserProfile();

      if (!profile.user.language_pair)
        navigate("/onboarding");
      else
        navigate("/profile");
    };
    handleOAuth();
  }, []);

  return <div>Авторизация...</div>;
}
