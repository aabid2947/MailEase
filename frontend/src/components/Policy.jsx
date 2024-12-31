import React, { useState } from "react";

const PrivacyPolicy = () => {
  const [isAccepted, setIsAccepted] = useState(false);

  const handleAccept = () => {
    setIsAccepted(true);
    // Handle logic on acceptance, e.g., saving to localStorage
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-semibold text-center text-gray-900 mb-6">Privacy Policy</h1>
      
      <div className="space-y-6 max-h-[500px] overflow-y-scroll px-2">
        <section>
          <h2 className="text-xl font-semibold text-gray-800">Your privacy is important to us.</h2>
          <p className="text-gray-600">
            It is MailEase's policy to respect your privacy regarding any information we may collect from you across our website, MailEase, and other sites we own and operate.
          </p>
        </section>

        <section>
          <h3 className="text-lg font-medium text-gray-700">1. Data Collection</h3>
          <p className="text-gray-600">
            We only ask for personal information when we truly need it to provide a service to you. We collect it by fair and lawful means, with your knowledge and consent.
          </p>
        </section>

        <section>
          <h3 className="text-lg font-medium text-gray-700">2. Data Retention</h3>
          <p className="text-gray-600">
            We only retain collected information for as long as necessary to provide you with your requested service.
          </p>
        </section>

        <section>
          <h3 className="text-lg font-medium text-gray-700">3. Data Security</h3>
          <p className="text-gray-600">
            What data we store, we’ll protect within commercially acceptable means to prevent loss and theft, as well as unauthorized access, disclosure, copying, use, or modification.
          </p>
        </section>

        <section>
          <h3 className="text-lg font-medium text-gray-700">4. Cookies</h3>
          <p className="text-gray-600">
            This site uses cookies to improve your experience. If you want to learn more about cookies and how we use them, please check our Cookie Policy.
          </p>
        </section>

        <section>
          <h3 className="text-lg font-medium text-gray-700">5. Third-Party Sharing</h3>
          <p className="text-gray-600">
            We don’t share any personally identifying information publicly or with third-parties, except when required by law.
          </p>
        </section>

        <section>
          <h3 className="text-lg font-medium text-gray-700">6. User Rights</h3>
          <p className="text-gray-600">
            You have the right to refuse our request for your personal information, with the understanding that we may be unable to provide some of the desired services.
          </p>
        </section>

        <section>
          <h3 className="text-lg font-medium text-gray-700">7. External Links</h3>
          <p className="text-gray-600">
            Our website may link to external sites that are not operated by us. We have no control over the content and practices of these sites.
          </p>
        </section>

        <section>
          <h3 className="text-lg font-medium text-gray-700">8. Acceptance</h3>
          <p className="text-gray-600">
            By using our services, you acknowledge that you agree with our privacy practices.
          </p>
        </section>

        {!isAccepted && (
          <button
            onClick={handleAccept}
            className="w-full bg-green-500 text-white py-2 rounded-md hover:bg-green-600 transition duration-300 mt-6"
          >
            Accept Privacy Policy
          </button>
        )}
      </div>

      {isAccepted && (
        <div className="text-center text-green-600 mt-4">
          <p>Thank you for accepting the Privacy Policy!</p>
        </div>
      )}
    </div>
  );
};

export default PrivacyPolicy;
