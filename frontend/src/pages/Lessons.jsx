import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../api/axios";
import {
  HiCheckCircle,
  HiLockClosed,
  HiLockOpen,
  HiUser,
} from "react-icons/hi";
import { AiFillCode } from "react-icons/ai";


export default function Lessons() {
  const navigate = useNavigate();
  const [lessons, setLessons] = useState([]);
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);


  const fetchData = async () => {
    try {
      const profileRes =
        await api.get("/protected");

      const lessonsRes =
        await api.get("/lessons/user");

      setProfile(profileRes.data.user);
      setLessons(lessonsRes.data.lessons);
    }

    catch (err) {
      console.error(err);
    }
  };

    const completedLessons = lessons.filter(
      lesson => lesson.status === "completed"
    ).length;

    const progressPercent = lessons.length
      ? Math.round((completedLessons / lessons.length) * 100)
      : 0;

  return (
    <div className="min-h-screen bg-bgPage px-6 py-8">
      {/* HEADER */}
        <div className="
            flex flex-col gap-4
            md:flex-row md:items-center md:justify-between
            mb-8
            px-6 py-4
            bg-white
            rounded-2xl
            shadow-xl
            border border-gray-100
          "
        >

          {/* LEFT SIDE */}
          <div className="flex flex-wrap items-center gap-4">

            {/* LANGUAGE PAIR */}
            <h1 className="text-lg sm:text-xl md:text-2xl font-bold whitespace-nowrap">
              <span className="text-primary">
                {profile?.language_pair?.lang1?.name}
              </span>

              <span className="text-gray-500 text-sm mx-2">
                vs
              </span>

              <span className="text-red-500">
                {profile?.language_pair?.lang2?.name}
              </span>
            </h1>


            {/* PROGRESSBAR */}
            <div
              className="
                relative
                h-5 sm:h-6
                w-full sm:w-48 md:w-64
                rounded-full
                bg-red-500
                shadow-inner
                overflow-hidden
                ring-1 ring-black/5
              "
            >
              <div
                className="h-full bg-primary transition-all duration-500 shadow-inner"
                style={{ width: `${progressPercent}%` }}
              />

              <span
                className="
                  absolute inset-0
                  flex items-center justify-center
                  text-xs sm:text-sm
                  font-semibold
                "
              >
                {progressPercent}%
              </span>
            </div>

          </div>


          {/* RIGHT SIDE BUTTONS */}
          <div className="flex gap-3 justify-center">

            <button
              onClick={() => navigate("/practice")}
              className="flex items-center gap-2
                border
                px-3 sm:px-5
                py-1.5 sm:py-2
                rounded-xl
                hover:bg-green-200
                hover:shadow-lg
                transition
                text-sm sm:text-base
              "
            >
                <AiFillCode className="text-3xl" />
                Практика
            </button>

            <button
              onClick={() => navigate("/profile")}
              className="flex items-center gap-2
                border
                px-3 sm:px-5
                py-1.5 sm:py-2
                rounded-xl
                hover:bg-green-200
                hover:shadow-lg
                transition
                text-sm sm:text-base
              "
            >
                <HiUser className="text-3xl" />
                Профиль
            </button>

          </div>

        </div>


      {/* LESSON GRID */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {lessons.map(lesson => (
          <LessonCard
            key={lesson.id}
            lesson={lesson}
          />
        ))}
      </div>

    </div>
  );
}


function LessonCard({ lesson }) {
  const navigate = useNavigate();

  const getStyles = () => {
    if (lesson.status === "completed") {
      return "bg-green-200 border-primary hover:shadow-lg cursor-pointer";
    }

    if (lesson.status === "available") {
      return "bg-white hover:shadow-lg cursor-pointer";
    }

    return "bg-red-200 border-red-500";
  };

  const handleClick = () => {
    if (lesson.status !== "locked") {
      navigate(`/lessons/${lesson.slug}`);
    }
  };

  return (
    <div
      onClick={handleClick}
      className={`relative rounded-2xl p-6 border ${getStyles()}`}
    >

      {/* TOP RIGHT STATUS */}
      <div className="absolute top-3 right-4 flex items-center gap-1 text-gray-400">

          <span>{lesson.order_index}</span>

          {lesson.status === "completed" && (
            <HiCheckCircle className="text-primary text-2xl" />
          )}

          {lesson.status === "available" && (
            <HiLockOpen className="text-primary text-2xl" />
          )}

          {lesson.status === "locked" && (
            <HiLockClosed className="text-red-500 text-2xl" />
          )}

        </div>

      {/* TITLE */}
      <h2 className="text-lg font-semibold">
        {lesson.title}
      </h2>

    </div>
  );
}