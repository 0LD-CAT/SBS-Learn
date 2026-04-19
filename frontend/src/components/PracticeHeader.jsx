import { useNavigate, useLocation } from "react-router-dom";
import { HiUser } from "react-icons/hi";
import { AiFillBook } from "react-icons/ai";
import { AiFillCode } from "react-icons/ai";


export default function PracticeHeader() {
  const location = useLocation();
  const navigate = useNavigate();

  const isProfilePage = location.pathname === "/profile";

  const buttonText = isProfilePage
      ? "Практика"
      : "Профиль";

  const buttonIcon = isProfilePage
      ? <AiFillCode className="text-3xl" />
      : <HiUser className="text-3xl" />;

  return (

    <div
      className="
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

      <h1 className="text-3xl font-extrabold tracking-tight">
          <span className="text-primary">Side</span>
          By
          <span className="text-red-500">Side</span>
          Learn
      </h1>


      {/* RIGHT SIDE BUTTONS */}

      <div className="flex gap-3 justify-center">

        <button
          onClick={() => navigate("/lessons")}
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
          <AiFillBook className="text-3xl" />
          Теория
        </button>


        <button
          onClick={() =>
            navigate(isProfilePage ? "/practice" : "/profile")
          }
          className="
            flex items-center gap-2
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
          {buttonIcon}
          {buttonText}
        </button>

      </div>

    </div>

  );

}