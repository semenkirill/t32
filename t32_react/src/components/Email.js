import React, { useEffect, useState } from 'react';
import useAuth from '../hooks/useAuth';
import axios from '../api/axios';

const MyAccount = () => {
    const { auth } = useAuth();
    const [email, setEmail] = useState('');

    useEffect(() => {
        const fetchMyAccount = async () => {
            try {
                const response = await axios.get('auth/users/me', {
                    headers: {
                        Authorization: `Bearer ${auth.accessToken}`, // Добавляем токен в заголовок
                    },
                });
                setEmail(response.data.email);
            } catch (error) {
                console.error('Error fetching user account:', error);
                // Обработка ошибки запроса, например, перенаправление на страницу с ошибкой
            }
        };

        if (auth?.accessToken) {
            fetchMyAccount();
        }
    }, [auth]);

    return (
        <section>
            <h1>My Account</h1>
            {email && (
                <p>
                    Welcome, {email}!
                </p>
            )}
        </section>
    );
};

export default MyAccount;
