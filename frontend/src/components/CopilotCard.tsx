import React, {useState} from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faArrowRight, faCookie, faExternalLink} from "@fortawesome/free-solid-svg-icons";

const save = () => {
    return <a href='/ai-models'
              className="px-6 py-3 bg-green-600 text-white rounded-md text-lg hover:bg-green-800 mx-2 mt-2 pt-2 float-right"
              style={{maxWidth: '100px !important'}}>Speichern</a>;
}

const listItemsStyle = () => {
    return 'ml-2 pl-2 mt-2 mb-2';
}

const CopilotCard: React.FC = () => {
    const [copied, setCopied] = useState<boolean>(false);
    const [cookie, setCookie] = useState<string>('');
    const code = '(function() {\n' +
        '  var cookies = document.cookie.split(\';\').map(function(cookie) {\n' +
        '    return cookie.trim();\n' +
        '  }).join(\'; \');\n' +
        '  console.log(cookies);\n' +
        '  return cookies;\n' +
        '})();';
    const copyToClipboard = async () => {
        try {
            await navigator.clipboard.writeText(code);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000); // Show "Copied" for 2 seconds
        } catch (err) {
            console.error('Failed to copy: ', err);
        }
    };

    return (<div className="bg-white p-6 rounded-lg shadow-lg">
        <h2 className="text-xl font-bold mb-4">Microsoft CoPilot Konfiguration</h2>
        <p className="text-gray-600">
            Für Copilot benötigen Sie einen validen Session cookie. Bitte folgen Sie folgenden
            Anweisungen:</p>
        <ol>
            <li className={listItemsStyle()}>1. Öffnen Sie <a className='text-blue-400'
                                                              href="https://copilot.microsoft.com"
                                                              target='_blank'
                                                              rel='noreferrer noopener'>Microsoft
                Copilot <FontAwesomeIcon className='ml-1' icon={faExternalLink}/></a>
            </li>
            <li className={listItemsStyle()}>2. Schicken Sie einige Nachrichten an CoPilot, bis die
                Captcha Validierung durchgeführt wurde.
            </li>
            <li className={listItemsStyle()}>3. Öffnen Sie ihre Browser-Konsole. Entweder:
                <ul>
                    <li className={listItemsStyle()}>a. Rechts-Click <FontAwesomeIcon
                        icon={faArrowRight}/> Untersuchen <FontAwesomeIcon
                        icon={faArrowRight}/> Konsole.
                    </li>
                    Oder
                    <li className={listItemsStyle()}>b. F12 Taste drücken (Chrome) und dann auf
                        Konsole
                    </li>
                </ul>
            </li>
            <li className={listItemsStyle()}>4. Kopieren Sie folgendes Code-Schnipsel, und fügen Sie es
                in der Konsole ein:
            </li>

            <div className="relative bg-gray-800 text-white rounded-lg overflow-hidden">
                {/* Copy button */}
                <button
                    onClick={copyToClipboard}
                    className="absolute top-2 right-2 bg-blue-600 text-sm px-3 py-1 rounded hover:bg-blue-500 focus:outline-none"
                >
                    {copied ? 'Copied!' : 'Copy'}
                </button>

                {/* Code display */}
                <pre className="p-4 overflow-x-auto">
                                <code>{code}</code>
                              </pre>
            </div>
            <li className={listItemsStyle()}>5. Schicken Sie das Schnipsel ab (mit Enter) und Kopieren
                sie die Ausgabe (Ohne Einführungszeichen). Fügen Sie die Ausgabe in die nachfolgende
                Text-Box und clicken Sie auf "Speichern".
            </li>
        </ol>
        <div>
            <label className="block text-sm font-semibold mb-1 mt-2" htmlFor="description">
                <FontAwesomeIcon icon={faCookie}/> Cookie von CoPilot Konsole:
            </label>
            <textarea
                id="description"
                value={cookie}
                onChange={(e) => setCookie(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-indigo-500"
                rows={4}
                placeholder="Cookie von CoPilot"
            />
        </div>
        {save()}
    </div>);
};

export default CopilotCard;