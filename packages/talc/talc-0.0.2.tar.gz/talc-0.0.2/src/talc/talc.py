import os
from datetime import datetime
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
import logging
import openai


class _SupabaseClient:
    def __init__(self):
        url: str = os.environ.get(
            "INSTANCE_URL", default="https://qdgodxkfxzzmzwfliahh.supabase.co"
        )
        key: str = os.environ.get(
            "INSTANCE_ANON_KEY",
            default="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFkZ29keGtmeHp6bXp3ZmxpYWhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODg0OTc0NzcsImV4cCI6MjAwNDA3MzQ3N30.4bgCdg77wwOJ9w1hOtCD-z0gBVGv8X_kIxBCr5KDCuA",
        )

        # API key format is organization:api_key
        talc_api_key: str = os.environ.get("TALC_API_KEY", default="")

        if talc_api_key == "":
            logging.warning(
                "TALC_API_KEY environment variable not set. Logging disabled."
            )
        organization, api_key = talc_api_key.split(":")
        self.__organization: str = organization

        options = ClientOptions(headers={"talckey": api_key})
        self.supabase: Client = create_client(url, key, options=options)

    def createSession(self):
        response = (
            self.supabase.table("sessions")
            .insert(
                {
                    "organization": self.__organization,
                }
            )
            .execute()
        )
        return response.data[0]["id"]

    def __createInput(self, sessionId, generationId, role, content, index):
        response = (
            self.supabase.table("inputs")
            .insert(
                {
                    "session": sessionId,
                    "generation": generationId,
                    "role": role,
                    "content": content,
                    "index": index,
                }
            )
            .execute()
        )
        return response.data[0]["id"]

    def __createGeneration(self, sessionId, content, agent, generated_at):
        response = (
            self.supabase.table("generations")
            .insert(
                {
                    "session": sessionId,
                    "content": content,
                    "agent": agent,
                    "generated_at": generated_at,
                }
            )
            .execute()
        )
        return response.data[0]["id"]

    def __historyArrayToInputs(self, history, generationId, sessionId):
        for index, chat in enumerate(history):
            self.__createInput(
                sessionId,
                generationId,
                chat["role"],
                chat["content"],
                # Index is reversed because we want the most recent message to have the lowest index
                len(history) - index,
            )

    def log(self, sessionId, history, generationContent, agent):
        generated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        generationId = self.__createGeneration(
            sessionId, generationContent, agent, generated_at
        )
        self.__historyArrayToInputs(history, generationId, sessionId)


def createSession():
    response = client.createSession()
    return response


def init():
    global client
    client = _SupabaseClient()


class __alternateCompletion(openai.ChatCompletion):
    @classmethod
    def create(cls, *args, **kwargs):
        # Pop arguments that are not supported by the original create method
        agent = kwargs.pop("agent", "Default")
        session = kwargs.pop("session", None)
        stream = "stream" in kwargs and kwargs["stream"]

        result = super().create(*args, **kwargs)

        # Handle case where we have received the full response at once.
        if not stream:
            try:
                if session and agent:
                    client.log(
                        session,
                        kwargs["messages"],
                        cls.__getContent(result.choices),
                        agent,
                    )
            except Exception as e:
                logging.warning("Error logging to talc: ", e)

            return result
        # Handle stream case
        else:
            logging.warning("Stream case not implemented yet.")
            # print("stream")
            # result = super().create(*args, **kwargs)

            # collected_chunks = []
            # collected_messages = []

            # for chunk in result:
            #     collected_chunks.append(chunk)
            #     chunk_message = chunk["choices"][0]["delta"]

            #     # Note: This probably doesn't work when streaming multiple
            #     # choices. Why would someone do that? We'll find out whenever
            #     # someone does it and this breaks.
            #     finished = chunk["choices"][0]["finish_reason"]
            #     collected_messages.append(chunk_message)

            #     if finished and session and agent:
            #         try:
            #             client.log(
            #                 session,
            #                 kwargs["messages"],
            #                 cls.__getContent(
            #                     "".join(
            #                         [m.get("content", "") for m in collected_messages]
            #                     )
            #                 ),
            #                 agent,
            #             )
            #         except Exception as e:
            #             logging.warning("Error logging to talc: ", e)

            #     yield chunk

    @classmethod
    async def acreate(cls, *args, **kwargs):
        # Pop arguments that are not supported by the original create method
        agent = kwargs.pop("agent", None)
        session = kwargs.pop("session", None)

        result = await super().acreate(*args, **kwargs)

        try:
            if session and agent:
                client.log(
                    session,
                    kwargs["messages"],
                    cls.__getContent(result.choices),
                    agent,
                )
        except Exception as e:
            logging.warning("Error logging to talc: ", e)

        return result

    @classmethod
    def __getContent(cls, choices):
        if len(choices) == 0:
            return ""
        elif "function_call" in choices[0].message:
            return choices[0].message.function_call
        return choices[0].message.content


openai.ChatCompletion = __alternateCompletion
