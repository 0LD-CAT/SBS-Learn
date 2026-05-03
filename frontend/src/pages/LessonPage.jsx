import { useEffect, useState, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api/axios";
import { getUserProfile } from "../api/user";

import FactBlock from "../components/FactBlock";
import ComparisonTable from "../components/ComparisonTable";
import CodeCompare from "../components/CodeCompare";
import InterestingFact from "../components/InterestingFact";
import Quiz from "../components/Quiz";
import Task from "../components/Task";

const LessonPage = () => {
  const { lessonId } = useParams();
  const navigate = useNavigate();

  const [lesson, setLesson] = useState(null);
  const [profile, setProfile] = useState(null);
  const [langs, setLangs] = useState(null);

  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [error, setError] = useState("");
  const [userLessons, setUserLessons] = useState([]);

  const quizRefs = useRef({});

  useEffect(() => {
      const fetchLessons = async () => {
        try {
          const res = await api.get("/lessons/user");
          setUserLessons(res.data.lessons);
        } catch (e) {
          console.error(e);
        }
      };

      fetchLessons();
  }, []);

  useEffect(() => {
      if (!userLessons.length) return;

      const lesson = userLessons.find(
        (l) => l.id === Number(lessonId)
      );

      if (!lesson || lesson.status === "locked") {
        navigate("/lessons", {
          state: { error: "Сначала пройди предыдущие уроки!" }
        });
      }
  }, [userLessons, lessonId]);

  useEffect(() => {
    const fetchUser = async () => {
      const data = await getUserProfile();

      setProfile(data.user);
      setLangs({
        left: data.user.language_pair.lang1,
        right: data.user.language_pair.lang2,
      });
    };

    fetchUser();
  }, []);

  useEffect(() => {
    if (!langs) return;

    const fetchLesson = async () => {
      const res = await api.get(`/lessons/${lessonId}/content`, {
        params: {
          left_lang: langs.left.slug,
          right_lang: langs.right.slug,
        },
      });

      setLesson(res.data);
    };

    fetchLesson();
  }, [langs, lessonId]);

  const handleAnswer = (index, data) => {
    setAnswers((prev) => ({
      ...prev,
      [index]: data,
    }));
  };

  const handleFinish = async () => {
    setShowResults(true);

    let firstErrorIndex = null;
    let hasError = false;

    Object.entries(answers).forEach(([index, a]) => {
      if (
        a.left === null ||
        a.right === null ||
        !a.leftCorrect ||
        !a.rightCorrect
      ) {
        hasError = true;
        if (firstErrorIndex === null) {
          firstErrorIndex = index;
        }
      }
    });

    if (hasError) {
      setError("Верно ответь на все вопросы перед завершением!");

      if (firstErrorIndex !== null) {
        quizRefs.current[firstErrorIndex]?.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      }

      return;
    }

    try {
      await api.post(`/lessons/${lessonId}/complete`);
      navigate("/lessons");
    } catch (e) {
      console.error(e);
    }
  };

  const renderBlock = (block, i) => {
    switch (block.type) {
      case "fact":
        return <FactBlock key={i} block={block} langs={langs} />;

      case "comparison_matrix":
        return <ComparisonTable key={i} block={block} langs={langs} />;

      case "side_by_side_code":
        return <CodeCompare key={i} block={block} />;

      case "interesting_fact":
        return <InterestingFact key={i} block={block} langs={langs} />;

      case "quiz_question":
        return (
          <div key={i} ref={(el) => (quizRefs.current[i] = el)}>
            <Quiz
              block={block}
              langs={langs}
              index={i}
              onAnswer={handleAnswer}
              showResults={showResults}
            />
          </div>
        );

      case "task":
        return <Task key={i} block={block} />;

      default:
        return null;
    }
  };

  if (!lesson || !langs) return <div className="p-6">Загрузка...</div>;

  return (
    <div className="min-h-screen bg-bgPage px-4 py-6">
      {/* HEADER */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between mb-8 px-6 py-4 bg-white rounded-2xl shadow-xl border border-gray-100">
        <button
          onClick={() => navigate(-1)}
          className="px-4 py-2 bg-gray-100 rounded-lg hover:bg-gray-200"
        >
          ← Назад
        </button>

        <div className="flex-1 text-center md:text-left">
          <h1 className="text-2xl font-bold">{lesson.title}</h1>
          <p className="text-gray-500">{lesson.description}</p>
        </div>

        <h1 className="
          w-full text-center
          md:w-auto md:text-left
          text-lg sm:text-xl md:text-2xl
          font-bold whitespace-nowrap
        ">
          <span className="text-primary">
            {profile?.language_pair?.lang1?.name}
          </span>

          <span className="text-gray-500 text-sm mx-2">vs</span>

          <span className="text-red-500">
            {profile?.language_pair?.lang2?.name}
          </span>
        </h1>
      </div>

      {/* CONTENT */}
      <div className="max-w-5xl mx-auto space-y-6">
        {lesson.blocks.map((block, i) => renderBlock(block, i))}
      </div>

      {/* ERROR */}
      {error && (
        <div className="text-center text-red-500 mt-6 font-semibold">
          {error}
        </div>
      )}

      {/* BUTTON */}
      <div className="max-w-5xl mx-auto mt-8">
        <button
          onClick={handleFinish}
          className="w-full py-3 bg-primary text-white rounded-xl hover:opacity-90"
        >
          Завершить урок
        </button>
      </div>
    </div>
  );
};

export default LessonPage;