import { useEffect, useState } from "react";
import Editor from "@monaco-editor/react";
import axios from "axios";

import { FiPlay } from "react-icons/fi";
import { MdRestartAlt } from "react-icons/md";


export default function CodePanel({ side, defaultLanguage }) {

  const [languages, setLanguages] = useState([]);
  const [language, setLanguage] = useState("");
  const [code, setCode] = useState("");
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [running, setRunning] = useState(false);
  const [runStatus, setRunStatus] = useState(null);
  const user_id = localStorage.getItem("user_id");

  const getLanguageConfig = (extension) => {
      return languages.find(
        lang => lang.extension === extension
      );
  };

  const resetCode = () => {
      if (!window.confirm(`Очистить код для ${language}?`)) return;

      localStorage.removeItem(
        `user_${user_id}_${side}_${language}_code`
      );

      const config = getLanguageConfig(language);

      if (config?.demo_code) {
          setCode(config.demo_code);
        }

        setInput("");
        setOutput("");
        setRunStatus(null);
      };

  const runCode = async () => {

  try {

    setRunning(true);
    setRunStatus(null);

    const response = await axios.post(
      "http://127.0.0.1:8000/piston/code/execute",
      {
        language,
        code,
        stdin: input
      }
    );

    const result = response.data;

    setOutput(result.output || result.message);

    if (result.stderr || result.status) {
      setRunStatus("error");
    } else {
      setRunStatus("success");
    }

  } catch (error) {

    setOutput("Ошибка соединения с сервером");
    setRunStatus("error");

  } finally {

    setRunning(false);

  }

};


  useEffect(() => {
      if (!languages.length) return;

      if (defaultLanguage) {
        setLanguage(defaultLanguage);
      } else {
        setLanguage(languages[0].extension);
      }
  }, [languages, defaultLanguage]);

  useEffect(() => {

    axios
      .get("http://127.0.0.1:8000/languages")
      .then(res => setLanguages(res.data.languages));

  }, []);

  useEffect(() => {
      if (!language || languages.length === 0)
        return;

      const savedCode = localStorage.getItem(`user_${user_id}_${side}_${language}_code`);

      if (savedCode) {
        setCode(savedCode);
      } else {

        const config = getLanguageConfig(language);

        if (config?.demo_code) {
          setCode(config.demo_code);
        }
      }
    }, [language, languages, side, user_id]);


  useEffect(() => {
      if (!user_id) return;

      localStorage.setItem(
        `user_${user_id}_${side}_${language}_code`,
        code
      );
}, [code, language, side, user_id]);


  return (

    <div className="w-full lg:w-1/2
                      h-[calc(95vh-140px)]
                      flex flex-col
                      gap-2">

      <div className="flex justify-between items-center
        bg-gray-50
        rounded-2xl
        px-3 py-2
        border">

        <div className="flex gap-2 items-center flex-wrap">
            {language && getLanguageConfig(language)?.icon_url && (
              <img
                src={getLanguageConfig(language).icon_url || "/default-lang.svg"}
                alt="lang"
                className="w-5 h-5"
              />
          )}
          <select
            className="border rounded-xl px-2 py-1"
            value={language}
            onChange={(e) =>
              setLanguage(e.target.value)
            }
          >

            {languages.map(lang => (

              <option
                key={lang.id}
                value={lang.extension}
              >
                {lang.name}
              </option>

            ))}

          </select>


          <button
              onClick={resetCode}
              className="flex items-center gap-1
              bg-red-100 text-red-600
              px-3 py-1
              rounded-lg
              hover:bg-red-200
              transition"
            >
              <MdRestartAlt />
              Сбросить
          </button>

        </div>


        <button
              onClick={runCode}
              disabled={running}
              className="flex items-center gap-1
              bg-primary text-white
              px-4 py-1
              rounded-lg
              hover:bg-green-400
              shadow-md
              disabled:bg-green-300
              transition"
            >
              <FiPlay />

              {running ? "Выполняется..." : "Выполнить"}
        </button>

      </div>


      {/* EDITOR */}

      <div className="
          flex-1
          border
          rounded-xl
          overflow-hidden
        ">
          <Editor
            height="100%"
            language={
              getLanguageConfig(language)?.slug
            }
            value={code}
            onChange={(value) => setCode(value)}
          />
        </div>


      {/* INPUT */}

      <label className="text-xs text-gray-400">
        INPUT
      </label>

      <textarea
          placeholder="Введите данные здесь..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="
            bg-white
            border
            rounded
            p-2
            h-20
            resize-none
            rounded-xl
          "
        />


      {/* OUTPUT */}

      <label className="text-xs text-gray-400 font-medium">
        OUTPUT
      </label>

      <textarea
          placeholder="Вывод..."
          value={output}
          readOnly
          className={`
              border
              rounded
              p-2
              h-28
              resize-none
              font-mono
              transition
              rounded-xl

              ${
                runStatus === "success"
                  ? "border-primary bg-green-50"
                  : runStatus === "error"
                  ? "border-red-500 bg-red-50"
                  : "border-gray-200 bg-gray-50"
              }
          `}
        />

    </div>

  );

}
