import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../api/axios";
import LanguageCard from "../components/LanguageCard";
import bookIcon from "../assets/book_icon.png";
import rocketIcon from "../assets/rocket_icon.png";
import targetIcon from "../assets/target_icon.png";


export default function Onboarding() {

  const navigate = useNavigate();

  const [languages, setLanguages] = useState([]);

  const [lang1, setLang1] = useState(null);
  const [lang2, setLang2] = useState(null);

  const selectedLang1 =
    languages.find(l => l.id === lang1);

  const selectedLang2 =
    languages.find(l => l.id === lang2);

  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        const res =
          await api.get("/languages");

        setLanguages(
          res.data.languages
        );
      }

      catch (error) {
        console.error(
          "Ошибка загрузки языков:",
          error
        );
      }
    };

    fetchLanguages();
  }, []);

  const handleSubmit = async () => {
    if (!lang1 || !lang2)
      return alert(
        "Выберите оба языка"
      );

    if (lang1 === lang2)
      return alert(
        "Выберите разные языки"
      );

    try {
      await api.post(
        "/select-languages-pair",
        {
          lang1_id: lang1,
          lang2_id: lang2
        }
      );

      navigate("/lessons");

    }

    catch (error) {
      console.error(
        "Ошибка выбора пары:",
        error
      );
    }
  };


  return (

    <div className="min-h-screen bg-bgPage flex flex-col items-center px-4 py-10">

      {/* HEADER */}
      <h1 className="text-3xl font-bold text-center">
        Добро пожаловать в приложение
        <br />
        <span className="text-green-500">
          Side
        </span>
            By
        <span className="text-red-500">
          Side
        </span>
        Learn!
      </h1>

      <p className="text-gray-500 mt-3 text-center max-w-lg">
        Освойте два языка программирования одновременно, сравнивая их бок-о-бок
      </p>


      {/* FEATURES */}
      <div className="mt-10 w-full max-w-5xl grid gap-6 md:grid-cols-3">

        <FeatureCard
          title="Side-by-side концепция"
          text="Сравнивайте синтаксис и шаблоны на разных языках"
          icon={bookIcon}
        />

        <FeatureCard
          title="Быстрое понимание"
          text="Поймите основные понятия, увидев различия"
          icon={rocketIcon}
        />

        <FeatureCard
          title="Практические примеры"
          text="Реальные примеры кода для каждой темы"
          icon={targetIcon}
        />

      </div>

    {/* LANGUAGE SELECT BLOCK */}
    <div className="bg-white shadow-xl rounded-2xl mt-10 p-6 w-full max-w-5xl">

      <h2 className="text-xl font-semibold text-center mb-6">
        Выберите ваши языки для начала обучения
      </h2>

      <div className="grid gap-6 md:grid-cols-2">

        {/* FIRST LANGUAGE */}
        <div>
          <label className="text-gray-600">
            Первый язык
          </label>

          <select
            className="w-full mt-2 border rounded-xl p-3"
            onChange={(e) =>
              setLang1(Number(e.target.value))
            }
          >
            <option>
              Выберите язык
            </option>

            {languages.map(lang => (

              <option
                key={lang.id}
                value={lang.id}
                disabled={lang.id === lang2}
              >
                {lang.name}
              </option>
            ))}
          </select>

          <div className="mt-4">
            <LanguageCard
              language={selectedLang1}
            />
          </div>
        </div>

        {/* SECOND LANGUAGE */}
        <div>
          <label className="text-gray-600">
            Второй язык
          </label>

          <select
            className="w-full mt-2 border rounded-xl p-3"
            onChange={(e) =>
              setLang2(Number(e.target.value))
            }
          >
            <option>
              Выберите язык
            </option>

            {languages.map(lang => (
              <option
                key={lang.id}
                value={lang.id}
                disabled={lang.id === lang1}
              >
                {lang.name}
              </option>
            ))}
          </select>

          <div className="mt-4">
            <LanguageCard
              language={selectedLang2}
            />
          </div>

        </div>

      </div>


      {/* BUTTON */}

      <button
        onClick={handleSubmit}
        className="w-full mt-8 bg-green-500 text-white py-3 rounded-xl font-medium hover:opacity-90"
      >

        Начать обучение!

      </button>

    </div>

    </div>
  );
}


/* FEATURE CARD COMPONENT */
function FeatureCard({ title, text, icon }) {
  return (
    <div className="bg-white rounded-2xl shadow-xl p-5 flex flex-col items-center text-center">

      <img src={icon} className="w-10 h-10" />

      <h3 className="font-bold mt-2">
        {title}
      </h3>

      <p className="text-gray-500 text-sm mt-1">
        {text}
      </p>

    </div>
  );
}
