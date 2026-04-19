import { useEffect, useState } from "react";

import { getUserProfile } from "../api/user";
import { logoutUser } from "../api/auth";
import PracticeHeader from "../components/PracticeHeader";
import { HiOutlineMail } from "react-icons/hi";
import { FiUser } from "react-icons/fi";
import { MdOutlineCode } from "react-icons/md";

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
      <div className="min-h-screen bg-bgPage">
        <PracticeHeader />

        <div className="flex items-center justify-center h-[70vh] text-gray-400">
          Загрузка профиля...
        </div>

      </div>
    );

  return (

    <div className="min-h-screen bg-bgPage px-6 py-8">

      <PracticeHeader />

      <div className="max-w-3xl mx-auto">

        {/* PROFILE CARD */}

        <div className="
          bg-white
          rounded-2xl
          shadow-xl
          border border-gray-100
          p-8
          flex flex-col gap-6
        ">

          {/* HEADER BLOCK */}

          <div className="flex items-center gap-5">

            {/* AVATAR */}

            <div className="
              w-16 h-16
              rounded-full
              bg-primary/10
              flex items-center justify-center
              text-primary
              text-2xl
              font-bold
            ">
              {user.username[0].toUpperCase()}
            </div>

            {/* NAME + EMAIL */}

            <div>

              <h1 className="text-2xl font-bold">
                {user.username}
              </h1>

              <div className="text-gray-400 text-sm">
                ID: {user.id}
              </div>

            </div>

          </div>


          {/* USER INFO GRID */}

          <div className="grid md:grid-cols-2 gap-4">

            {/* EMAIL */}

            <div className="
              flex items-center gap-3
              bg-gray-50
              rounded-xl
              px-4 py-3
            ">

              <HiOutlineMail className="text-gray-500 text-xl" />

              <div>

                <div className="text-xs text-gray-400">
                  Email
                </div>

                <div className="font-medium">
                  {user.email}
                </div>

              </div>

            </div>


            {/* LANGUAGE PAIR */}

            <div className="
              flex items-center gap-3
              bg-gray-50
              rounded-xl
              px-4 py-3
            ">

              <MdOutlineCode className="text-gray-500 text-xl" />

              <div>

                <div className="text-xs text-gray-400">
                  Пара языков
                </div>

                <div className="font-medium">

                  {user.language_pair
                    ? `${user.language_pair.lang1.name} vs ${user.language_pair.lang2.name}`
                    : "Не выбрана"}

                </div>

              </div>

            </div>

          </div>


          {/* ACTIONS */}

          <div className="flex justify-end pt-4">

            <button

              onClick={logoutUser}

              className="
                flex items-center gap-2
                px-5 py-2
                rounded-xl
                bg-red-500
                hover:bg-red-600
                text-white
                shadow-md
                transition
              "

            >

              Выйти

            </button>

          </div>

        </div>

      </div>

    </div>

  );

}