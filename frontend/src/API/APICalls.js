import axios from "axios";

const URL = 'http://127.0.0.1:8000'
export const AutheticateUser = async (formData) => {
    try {
        console.log("FormData contents:");
        for (let [key, value] of formData.entries()) {
            console.log(`${key}:`, value);
        }
        const response = await axios.post(`${URL}/authenticate`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
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
        const response = await axios.post(`${URL}/monitor-mails`,{preference:preference});


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


