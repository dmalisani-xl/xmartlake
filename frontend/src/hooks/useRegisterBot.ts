import { useEffect, useState } from "react";
import { ApiService } from "networking/api-service";
import { API_ROUTES } from "networking/api-routes";
import { constants } from "config/constants";

export const useRegisterBot = () : [boolean, (bot: NewBotData) => Promise<void>, string]=> {
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const COORDINATOR_URL = 'http://coordinator:7000' 

  const registerBot = async (bot: NewBotData) => {
    setLoading(true);
    try {
      const url = `${COORDINATOR_URL}${API_ROUTES.REGISTER}`;
      await ApiService.post(url, bot, {
        headers: {
          'Access-Control-Allow-Origin': '*',
        }
      });
    } catch (error) {
      setErrorMessage("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };


  return [loading, registerBot, errorMessage] ;
}