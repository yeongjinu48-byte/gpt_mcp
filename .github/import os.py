import os
import json
import requests
import sys
import logging

# 디버그 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_env_vars():
    """환경 변수 검사"""
    required_vars = ["RUBE_BASE", "RUBE_AUTH"]
    missing = [var for var in required_vars if var not in os.environ]
    if missing:
        logger.error(f"필수 환경 변수가 없습니다: {', '.join(missing)}")
        sys.exit(1)
    else:
        logger.info("인증이 성공적으로 완료되었습니다!")
        logger.info(f"RUBE_BASE: {os.environ['RUBE_BASE']}")

def create_default_macro():
    """기본 매크로 설정 생성"""
    return {
        "steps": [
            {
                "name": "NEW_SESSION",
                "path": "/NEW_SESSION",  # 실제 MCP API 경로로 수정 필요
                "args": "{}"
            },
            {
                "name": "CONNECTIONS_CHECK",
                "path": "/RUBE_MANAGE_CONNECTIONS",
                "args": '{"session_id": "$SID"}'
            }
        ]
    }

def run_macro():
    """매크로 실행"""
    check_env_vars()
    
    base_url = os.environ["RUBE_BASE"]
    auth_token = os.environ["RUBE_AUTH"]
    
    try:
        with open("macro.json", "r", encoding="utf-8") as f:
            macro = json.load(f)
            logger.info("\n기존 macro.json 파일을 불러왔습니다")
    except FileNotFoundError:
        logger.info("\n기본 macro.json 파일을 생성합니다...")
        macro = create_default_macro()
        with open("macro.json", "w", encoding="utf-8") as f:
            json.dump(macro, f, indent=2, ensure_ascii=False)
    
    session_id = None
    for step in macro["steps"]:
        logger.info(f"\n실행 단계: {step['name']}")
        
        try:
            args = json.loads(step["args"].replace("$SID", session_id if session_id else ""))
            url = f"{base_url}{step['path']}"
            
            headers = {
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, headers=headers, json=args)
            response.raise_for_status()
            result = response.json()
            
            if step["name"] == "NEW_SESSION":
                session_id = result.get("session_id")
                if session_id:
                    logger.info(f"새 세션이 생성되었습니다: {session_id}")
            
            logger.info(f"성공: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        except Exception as e:
            logger.error(f"\n오류 발생 ({step['name']}):")
            logger.error(str(e))
            logger.error(f"요청 URL: {url}")
            logger.error(f"요청 데이터: {args}")
            sys.exit(1)

def main():
    """메인 함수"""
    logger.info("매크로 실행을 시작합니다...")
    run_macro()
    logger.info("\n매크로 실행이 완료되었습니다.")

if __name__ == "__main__":
    main()