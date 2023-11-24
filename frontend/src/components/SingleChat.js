import { FormControl } from "@chakra-ui/form-control";
import { Input } from "@chakra-ui/input";
import { Box, Text } from "@chakra-ui/layout";
import "./styles.css";
import { IconButton, Spinner, useToast } from "@chakra-ui/react";
import { getSender, getSenderFull } from "../config/ChatLogics";
import { useEffect, useState } from "react";
import axios from "axios";
import { ArrowBackIcon } from "@chakra-ui/icons";
import ProfileModal from "./miscellaneous/ProfileModal";
import ScrollableChat from "./ScrollableChat";
import Lottie from "react-lottie";
import animationData from "../animations/typing.json";
import { useParams } from "react-router-dom";

import io from "socket.io-client";
import UpdateGroupChatModal from "./miscellaneous/UpdateGroupChatModal";
import { ChatState } from "../Context/ChatProvider";
const ENDPOINT = "http://localhost:5000"; // "https://talk-a-tive.herokuapp.com"; -> After deployment
var socket, selectedChatCompare;

const SingleChat = ({ fetchAgain, setFetchAgain }) => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [newMessage, setNewMessage] = useState("");
  const [socketConnected, setSocketConnected] = useState(false);
  const [typing, setTyping] = useState(false);
  const [istyping, setIsTyping] = useState(false);
  const toast = useToast();
  const url = process.env.REACT_APP_API_URL;
  const wsurlenv=process.env.REACT_APP_WS_URL;
  const {room_id}=useParams()

  const wsurl=`ws://${wsurlenv}/ws/`


  const [socket, setSocket] = useState(null);
  const [typingSocket,setTypingSocket]=useState(null)
  const [chatSocket,setChatSocket]=useState(null)

      


  const defaultOptions = {
    loop: true,
    autoplay: true,
    animationData: animationData,
    rendererSettings: {
      preserveAspectRatio: "xMidYMid slice",
    },
  };
  const { selectedChat, setSelectedChat, user, notification, setNotification } =
    ChatState();

  const fetchMessages = async () => {
    if (!selectedChat) return;

    
      const config = {
        headers: {
          Authorization: `Token ${user.token}`,
        },
      };

      setLoading(true);

      axios.get(url+`message/${selectedChat.id}/`,config)
      .then((res)=>{
        setMessages(res.data);
        setLoading(false);

        // socket.emit("join chat", selectedChat.id);
        chatSocket.send(["join chat",selectedChat.id]);

      })
      .catch ((error)=> {
        toast({
          title: "Error Occured!",
          description: "Failed to Load the Messages",
          status: "error",
          duration: 5000,
          isClosable: true,
          position: "bottom",
        });
    })
  };

  const sendMessage = async (event) => {
    if (event.key === "Enter" && newMessage) {
        typingSocket.send([false,user.username]);

      // socket.emit("stop typing", selectedChat._id);
        const config = {
          headers: {
            "Content-type": "application/json",
            Authorization: `Token ${user.token}`,
          },
        };
        setNewMessage("");
        await axios.post(url+"message/"+selectedChat.id+"/",
          {
            content: newMessage,
            // chatId: selectedChat,
          },
          config
        )
        .then((res)=>{
          setMessages([...messages, res.data]);
          chatSocket.send(res.data)
        })
        // socket.emit("new message", data);
        .catch ((error)=> {
          toast({
            title: "Error Occured!",
            description: "Failed to send the Message",
            status: "error",
            duration: 5000,
            isClosable: true,
            position: "bottom",
          });
      })
    }
  };

  useEffect(() => {

    
    const typingSocket = new WebSocket(wsurl+'typing/'+selectedChat?.id+'/');
    

    setTypingSocket(typingSocket)
    typingSocket.addEventListener('open', (event) => {
      console.log('WebSocket connection opened:', event);
      setSocketConnected(true)
    });

    // typingSocket.addEventListener('typing', (event) => {
    //   // setIsTyping(true)
    // });
    typingSocket.addEventListener('message', (event) => {
      const data=JSON.parse(event.data)
      console.log(data)
      if(data.username!==user.username){
        setIsTyping(data.is_typing)
      }
    });

  
    typingSocket.addEventListener('close', (event) => {
      console.log('WebSocket connection closed:', event);
    });

    // return () => {
    // // Clean up the WebSocket connection when the component is unmounted or dependencies change
    //   typingSocket.close();
    //   setSocketConnected(false);
    // };


    // socket = io(ENDPOINT);
    // socket.emit("setup", user);
    // socket.on("connected", () => setSocketConnected(true));
    // socket.on("typing", () => setIsTyping(true));
    // socket.on("stop typing", () => setIsTyping(false));

    // eslint-disable-next-line
  }, [selectedChat]);

  useEffect(() => {
    const chatSocket=new WebSocket(wsurl+'chat/'+selectedChat?.id+'/')
    console.log(chatSocket)
    chatSocket.addEventListener('open', (event) => {
      console.log('WebSocket connection opened:', event);
    });
    fetchMessages();

    selectedChatCompare = selectedChat;
    // eslint-disable-next-line
  },[selectedChat]);


  useEffect(()=>{
    const chatSocket=new WebSocket(wsurl+'chat/'+selectedChat?.id+'/')
    console.log(chatSocket)
    setChatSocket(chatSocket)
  },[])

  useEffect(() => {
    chatSocket?.addEventListener('message', (event) => {
      const newMessageRecieved=event.data
      if (
        !selectedChatCompare || // if chat is not selected or doesn't match current chat
        selectedChatCompare.id !== newMessageRecieved.room
      ) {
        if (!notification.includes(newMessageRecieved)) {
          setNotification([newMessageRecieved, ...notification]);
          setFetchAgain(!fetchAgain);
        }
      } else {
        setMessages([...messages, newMessageRecieved]);
      }
    });

  
    chatSocket?.addEventListener('close', (event) => {
      console.log('WebSocket connection closed:', event);
    });


  });

  const typingHandler = (e) => {
    setNewMessage(e.target.value);

    if (!socketConnected) return;

    if (!typing) {
      setTyping(true);
        typingSocket.send([true,user.username]);

      // socket.emit("typing", selectedChat._id);
    }
    let lastTypingTime = new Date().getTime();
    var timerLength = 3000;
    setTimeout(() => {
      var timeNow = new Date().getTime();
      var timeDiff = timeNow - lastTypingTime;
      if (timeDiff >= timerLength && typing) {
        // socket.emit("stop typing", selectedChat._id);
        setTyping(false);
        typingSocket.send([false,user.username]);
      }
    }, timerLength);
  };

  return (
    <>
      {selectedChat ? (
        <>
          <Text
            fontSize={{ base: "28px", md: "30px" }}
            pb={3}
            px={2}
            w="100%"
            fontFamily="Work sans"
            d="flex"
            justifyContent={{ base: "space-between" }}
            alignItems="center"
          >
            <IconButton
              d={{ base: "flex", md: "none" }}
              icon={<ArrowBackIcon />}
              onClick={() => setSelectedChat("")}
            />
            {messages &&
              (!selectedChat.isGroupChat ? (
                <>
                  {getSender(user, selectedChat.users)}
                  <ProfileModal
                    user={getSenderFull(user, selectedChat.users)}
                  />
                </>
              ) : (
                <>
                  {selectedChat.name_room.toUpperCase()}
                  <UpdateGroupChatModal
                    fetchMessages={fetchMessages}
                    fetchAgain={fetchAgain}
                    setFetchAgain={setFetchAgain}
                  />
                </>
              ))}
          </Text>
          <Box
            d="flex"
            flexDir="column"
            justifyContent="flex-end"
            p={3}
            bg="#E8E8E8"
            w="100%"
            h="100%"
            borderRadius="lg"
            overflowY="hidden"
          >
            {loading ? (
              <Spinner
                size="xl"
                w={20}
                h={20}
                alignSelf="center"
                margin="auto"
              />
            ) : (
              <div className="messages">
                <ScrollableChat messages={messages} />
              </div>
            )}

            <FormControl
              onKeyDown={sendMessage}
              id="first-name"
              isRequired
              mt={3}
            >
              {istyping ? (
                <div>
                  <Lottie
                    options={defaultOptions}
                    // height={50}
                    width={70}
                    style={{ marginBottom: 15, marginLeft: 0 }}
                  />
                </div>
              ) : (
                <div></div>
              )}
              <Input
                variant="filled"
                bg="#E0E0E0"
                placeholder="Enter a message.."
                value={newMessage}
                onChange={typingHandler}
              />
            </FormControl>
          </Box>
        </>
      ) : (
        // to get socket.io on same page
        <Box d="flex" alignItems="center" justifyContent="center" h="100%">
          <Text fontSize="3xl" pb={3} fontFamily="Work sans">
            Click on a user to start chatting
          </Text>
        </Box>
      )}
    </>
  );
};

export default SingleChat;
