const express = require('express');
const AWS = require('aws-sdk');
const bodyParser = require('body-parser');
const axios = require('axios');
require('dotenv').config();

const app = express();
app.use(bodyParser.json());

AWS.config.update({
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    region: process.env.AWS_REGION
});

const ses = new AWS.SES();

app.post('/send-email', async (req, res) => {
    const { subject, text } = req.body;

    try {
        const response = await axios.get('http://localhost:5000/preferences');
        const users = response.data;

        users.forEach(user => {
            if (user.notification_preference === 'email' && user.status === 'active') {
                const params = {
                    Source: process.env.SENDER_EMAIL,
                    Destination: { ToAddresses: [user.email] },
                    Message: {
                        Subject: { Data: subject },
                        Body: { Text: { Data: text } }
                    }
                };

                ses.sendEmail(params, (err, data) => {
                    if (err) {
                        console.error(`Error sending email to ${user.email}:`, err);
                    } else {
                        console.log(`Email sent to ${user.email}`);
                    }
                });
            }
        });

        res.status(200).send('Emails sent');
    } catch (error) {
        console.error('Error fetching user preferences:', error);
        res.status(500).send('Error sending emails');
    }
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
