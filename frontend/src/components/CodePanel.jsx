import { useEffect, useState } from "react";
import Editor from "@monaco-editor/react";
import axios from "axios";


export default function CodePanel({ side, defaultLanguage }) {

  const [languages, setLanguages] = useState([]);
  const [language, setLanguage] = useState("");
  const [code, setCode] = useState("");
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [running, setRunning] = useState(false);

  const getLanguageConfig = (extension) => {
      return languages.find(
        lang => lang.extension === extension
      );
  };

  const resetCode = () => {
      if (!window.confirm("Очистить код?")) return;

      localStorage.removeItem(
        `${side}_${language}_code`
      );

      const config = getLanguageConfig(language);

      if (config?.demo_code) {
        setCode(config.demo_code);
      }
  };

  const runCode = async () => {

    setRunning(true);

    const response = await axios.post(
      "http://127.0.0.1:8000/piston/code/execute",
      {
        language,
        code,
        stdin: input
      }
    );

    setOutput(response.data.output);

    setRunning(false);

  };


  useEffect(() => {

      if (defaultLanguage) {

        setLanguage(defaultLanguage);

      }

  }, [defaultLanguage]);

  useEffect(() => {
      if (languages.length > 0 && !language) {

        setLanguage(languages[0].extension);

      }
    }, [languages]);

  useEffect(() => {

    axios
      .get("http://127.0.0.1:8000/languages")
      .then(res => setLanguages(res.data.languages));

  }, []);

  useEffect(() => {
      if (!language || languages.length === 0)
        return;

      const savedCode =
        localStorage.getItem(`${side}_${language}_code`);

      if (savedCode) {
        setCode(savedCode);
      } else {

        const config = getLanguageConfig(language);

        if (config?.demo_code) {
          setCode(config.demo_code);
        }
      }
    }, [language, languages, side]);


  useEffect(() => {

    localStorage.setItem(
      `${side}_${language}_code`,
      code
    );

  }, [code, language, side]);


  return (

    <div className="w-full lg:w-1/2
                      h-[calc(95vh-140px)]
                      flex flex-col
                      gap-2">

      <div className="flex justify-between items-center">

        <div className="flex gap-2">

          <select
            className="border rounded px-2 py-1"
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
            className="bg-red-500 border px-3 py-1 rounded hover:bg-red-400"
          >
            Очистить
          </button>

        </div>


        <button
          onClick={runCode}
          disabled={running}
          className="bg-primary text-white px-4 py-1 rounded hover:bg-green-400 disabled:bg-green-400"
        >
          {running ? "Выполняется..." : "Выполнить ▶"}
        </button>

      </div>


      {/* EDITOR */}

      <div className="
          flex-1
          border
          rounded
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

      <textarea
          placeholder="Введите данные здесь..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="
            border
            rounded
            p-2
            h-20
            resize-none
          "
        />


      {/* OUTPUT */}

      <textarea
          placeholder="Вывод..."
          value={output}
          readOnly
          className="
            border
            rounded
            p-2
            h-28
            resize-none
            bg-gray-50
          "
        />

    </div>

  );

}
