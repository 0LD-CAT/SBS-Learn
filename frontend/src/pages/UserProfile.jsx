import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { getUserProfile } from "../api/user";
import { logoutUser } from "../api/auth";
import PracticeHeader from "../components/PracticeHeader";
import { HiOutlineMail } from "react-icons/hi";
import { MdOutlineCode } from "react-icons/md";
import { FiCheckCircle, FiClock, FiLock } from "react-icons/fi";

export default function Profile() {
  const [user, setUser] = useState(null);
  const [progress, setProgress] = useState([]);
  const navigate = useNavigate();

  const handleChangeLanguages = () => {
    const confirmed = window.confirm(
      "Вы уверены, что хотите изменить языковую пару для изучения?"
    );

    if (confirmed) {
      navigate("/onboarding");
    }
  };

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await getUserProfile();
        setUser(data.user);
      } catch (error) {
        console.error(error);
      }
    };

    const fetchProgress = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/lessons/progress", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });

        const data = await res.json();
        setProgress(data.progress);
      } catch (e) {
        console.error(e);
      }
    };

    fetchProfile();
    fetchProgress();
  }, []);

  if (!user)
    return (
      <div className="min-h-screen bg-bgPage">
        <PracticeHeader />
        <div className="flex items-center justify-center h-[70vh] text-gray-400">
          Загрузка профиля...
        </div>
      </div>
    );

  const formatSlug = (slug) =>
    slug
      ?.replaceAll("-", " ")
      .replace("vs", "vs")
      .toUpperCase();

  const totalProgress =
    progress.length > 0
      ? Math.round(
          progress.reduce((acc, p) => acc + p.progress, 0) /
            progress.length
        )
      : 0;

  const renderStatus = (progress) => {
      if (progress === 100) {
        return (
          <div className="flex items-center gap-1 text-primary text-xs mt-1">
            <FiCheckCircle />
            <span>Завершено</span>
          </div>
        );
      }

      if (progress > 0 && progress < 100) {
        return (
          <div className="flex items-center gap-1 text-blue-400 text-xs mt-1">
            <FiClock />
            <span>В процессе</span>
          </div>
        );
      }

      return (
        <div className="flex items-center gap-1 text-gray-400 text-xs mt-1">
          <FiLock />
          <span>Не начато</span>
        </div>
      );
  };

  return (
    <div className="min-h-screen bg-bgPage px-6 py-8">
      <PracticeHeader />

      <div className="max-w-3xl mx-auto">

        {/* PROFILE CARD */}
        <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8 flex flex-col gap-6">

          {/* HEADER */}
          <div className="flex items-center gap-5">

            <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center text-primary text-2xl font-bold">
              {user.username[0].toUpperCase()}
            </div>

            <div>
              <h1 className="text-2xl font-bold">{user.username}</h1>
              <div className="text-gray-400 text-sm">ID: {user.id}</div>
            </div>

          </div>

          {/* INFO */}
          <div className="grid md:grid-cols-2 gap-4">

            <div className="flex items-center gap-3 bg-gray-50 rounded-xl px-4 py-3">
              <HiOutlineMail className="text-gray-500 text-xl" />
              <div>
                <div className="text-xs text-gray-400">Email</div>
                <div className="font-medium">{user.email}</div>
              </div>
            </div>

            {/* LANGUAGE PAIR */}
            <div className="flex items-center justify-between bg-gray-50 rounded-xl px-4 py-3">
              <div className="flex items-center gap-3">
                <MdOutlineCode className="text-gray-500 text-xl" />
                <div>
                  <div className="text-xs text-gray-400">Пара языков</div>
                  <div className="font-medium">
                    {user.language_pair
                      ? `${user.language_pair.lang1.name} vs ${user.language_pair.lang2.name}`
                      : "Не выбрана"}
                  </div>
                </div>
              </div>

              <button
                onClick={handleChangeLanguages}
                className="text-sm px-3 py-1.5 rounded-lg bg-primary/10 text-primary hover:bg-primary/20 transition"
              >
                Изменить
              </button>
            </div>
          </div>

          {/* OVERALL PROGRESS (DUOLINGO STYLE) */}
          <div className="pt-4 border-t border-gray-100">

            <div className="flex justify-between items-center mb-2">
              <h2 className="text-sm font-semibold text-gray-500">
                Общий прогресс
              </h2>

              <span className="text-sm font-medium text-primary">
                {totalProgress}%
              </span>
            </div>

            <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-primary transition-all duration-700"
                style={{ width: `${totalProgress}%` }}
              />
            </div>
          </div>

          {/* PROGRESS BY LANGUAGE PAIR */}
          <div className="pt-4 border-t border-gray-100">

            <h2 className="text-sm font-semibold text-gray-500 mb-4">
              Прогресс по языковым парам
            </h2>

            <div className="space-y-4">

              {progress.map((p) => (
                <div key={p.language_pair_id}>

                  {/* HEADER */}
                  <div className="flex justify-between text-sm mb-1">

                    <span className="font-medium text-gray-700">
                      {formatSlug(p.slug)}
                    </span>

                    <span className="text-gray-500">
                      {p.progress}%
                    </span>

                  </div>

                  {/* BAR */}
                  <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-primary transition-all duration-700"
                      style={{ width: `${p.progress}%` }}
                    />
                  </div>

                  {/* STATUS */}
                  <div className="text-xs mt-1 text-gray-400">

                    {renderStatus(p.progress)}

                  </div>

                </div>
              ))}

            </div>
          </div>

          {/* ACTIONS */}
          <div className="flex justify-end pt-4">
            <button
              onClick={logoutUser}
              className="flex items-center gap-2 px-5 py-2 rounded-xl bg-red-500 hover:bg-red-600 text-white shadow-md transition"
            >
              Выйти
            </button>
          </div>

        </div>
      </div>
    </div>
  );
}