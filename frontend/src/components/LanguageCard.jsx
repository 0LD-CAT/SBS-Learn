export default function LanguageCard({ language }) {

  if (!language)
    return null;

  return (
    <div className="bg-white rounded-xl shadow-xl p-5 flex items-center gap-4 transition hover:shadow-lg">
      {/* ICON */}
      <img
        src={language.icon_url}
        alt={language.name}
        className="w-12 h-12 object-contain shrink-0"
      />

      {/* TEXT */}
      <div>
        <h3 className="font-semibold text-lg">
          {language.name}
        </h3>

        <p className="text-gray-500 text-sm mt-1">
          {language.description}
        </p>
      </div>

    </div>
  );
}