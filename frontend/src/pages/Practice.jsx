import CodePanel from "../components/CodePanel";
import PracticeHeader from "../components/PracticeHeader";


export default function Practice() {

  return (
    <div className="min-h-screen bg-bgPage px-6 py-8">
      <PracticeHeader />
      <div className="
          flex
          flex-col
          lg:flex-row
          gap-4
        ">
          <CodePanel side="left"/>
          <CodePanel side="right" defaultLanguage="cpp"/>
      </div>
    </div>
  );

}