import axios from "axios";

const URL = 'https://mailease-backend-cy701ifgn-aabid2947s-projects.vercel.app';
const VERSEL_SECRET_KEY = 'vCD24dEZQ0Ej8TnuMf9gccSqq4AZgpvF'; // Secret for protection bypass

// Utility function to add protection bypass headers
const getHeaders = () => {
    return {
        'Content-Type': 'multipart/form-data',
        'x-vercel-protection-bypass': VERSEL_SECRET_KEY,
    };
}

export const AutheticateUser = async (formData) => {
    try {
        console.log("Sending to URL:", `${URL}/authenticate`);
        console.log("Form data:", formData);
        console.log("Headers:", getHeaders());

        for (let [key, value] of formData.entries()) {
            console.log(`${key}:`, value);
        }

        const response = await axios.post(`${URL}/authenticate`, formData, {
            headers: getHeaders(),
        });

        return response;
    } catch (error) {
        console.log(error)
        return error;
    }
}

export const MonitorEmails = async (preferences, interval) => {
    try {
        console.log("Preferences:", preferences);
        const preference = {
            email_addresses: preferences.email_addresses,
            keywords: preferences.keywords,
            user_phone_number: preferences.user_phone_number,
            interval: interval,
            uuid: preferences.uuid
        }

        const response = await axios.post(`${URL}/monitor-mails`, { preference: preference }, {
            headers: getHeaders(),  // Include headers here too
        });

        if (response.data.status === "success") {
            return response;
        } else {
            return response;
        }
    } catch (error) {
        console.error('Error monitoring emails:', error);
    }
}

export const DeleteEmails = async (criteria) => {
    try {
        const response = await axios.post(`${URL}/delete-emails`, {
            criteria: criteria,
        }, {
            headers: getHeaders(),  // Include headers here too
        });

        if (response.data.status === "success") {
            console.log('Email deletion process completed!');
        } else {
            console.log('Error: ' + response.data.message);
        }
    } catch (error) {
        console.error('Error deleting emails:', error);
        alert('Error deleting emails');
    }
}
