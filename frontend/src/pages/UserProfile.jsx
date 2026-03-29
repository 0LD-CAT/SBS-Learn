import { useEffect, useState } from "react";

import { getUserProfile } from "../api/user";
import { logoutUser } from "../api/auth";


export default function Profile() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await getUserProfile();
        setUser(data.user);
      } catch (error) {
        console.error(error);
      }
    };

    fetchProfile();
  }, []);

  if (!user)
    return (
      <div className="min-h-screen flex items-center justify-center">
        Загрузка профиля...
      </div>
    );

  return (
    <div className="min-h-screen flex items-center justify-center bg-bgPage">
      <div className="bg-white shadow-card rounded-2xl p-8 w-full max-w-md">

        <h1 className="text-xl font-bold mb-4">
          Профиль пользователя
        </h1>

        <p>
          <strong>ID:</strong> {user.id}
        </p>

        <p>
          <strong>Username:</strong> {user.username}
        </p>

        <p>
          <strong>Email:</strong> {user.email}
        </p>

        <p>
          <strong>Пара ЯП для изучения:</strong>{" "}
          {user.language_pair? `${user.language_pair.lang1.name} vs ${user.language_pair.lang2.name}` : "Не выбрана"}
        </p>

        <button onClick={logoutUser} className="mt-6 w-full bg-red-500 hover:bg-red-600 text-white py-3 rounded-lg transition">
            Выйти
        </button>

      </div>
    </div>
  );
}