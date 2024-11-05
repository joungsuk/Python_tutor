import socket
import threading
import logging
from typing import Tuple, Optional
import signal
import sys

class SocketServer:
    def __init__(self, host: str = '127.0.0.1', port: int = 9999):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.running = False
        
        # 로깅 설정
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # 시그널 핸들러 설정
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def setup_server(self) -> None:
        """서버 소켓 설정"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)  # 연결 대기 큐 크기 설정
            logging.info(f'서버가 {self.host}:{self.port}에서 시작되었습니다.')
        except Exception as e:
            logging.error(f'서버 설정 중 오류 발생: {e}')
            sys.exit(1)

    def handle_client(self, client_socket: socket.socket, addr: Tuple[str, int]) -> None:
        """클라이언트 처리"""
        try:
            logging.info(f'클라이언트 연결됨: {addr}')
            while self.running:
                data = client_socket.recv(4096)  # 버퍼 크기 증가
                if not data:
                    break
                
                message = data.decode('utf-8', errors='ignore')
                logging.info(f'수신 ({addr}): {message}')
                
                # 에코 응답
                client_socket.sendall(data)
                
        except ConnectionResetError:
            logging.warning(f'클라이언트 연결 끊김: {addr}')
        except Exception as e:
            logging.error(f'클라이언트 처리 중 오류 발생: {e}')
        finally:
            client_socket.close()
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            logging.info(f'클라이언트 연결 종료: {addr}')

    def start(self) -> None:
        """서버 시작"""
        self.running = True
        self.setup_server()
        
        try:
            while self.running:
                try:
                    client_socket, addr = self.server_socket.accept()
                    self.clients.append(client_socket)
                    
                    # 새로운 스레드에서 클라이언트 처리
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, addr)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:  # 정상적인 종료가 아닌 경우에만 에러 로깅
                        logging.error(f'클라이언트 수락 중 오류 발생: {e}')
                        
        except KeyboardInterrupt:
            logging.info('서버 종료 요청됨')
        finally:
            self.cleanup()

    def cleanup(self) -> None:
        """서버 정리"""
        self.running = False
        
        # 모든 클라이언트 연결 종료
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        self.clients.clear()
        
        # 서버 소켓 종료
        if self.server_socket:
            self.server_socket.close()
        logging.info('서버가 정상적으로 종료되었습니다.')

    def signal_handler(self, signum: int, frame) -> None:
        """시그널 처리"""
        logging.info(f'시그널 {signum} 수신, 서버를 종료합니다.')
        self.cleanup()
        sys.exit(0)

if __name__ == "__main__":
    server = SocketServer()
    server.start() 