import UIKit
import KakaoSDKAuth

class SceneDelegate: UIResponder, UIWindowSceneDelegate {

    var window: UIWindow?

    func scene(_ scene: UIScene, openURLContexts URLContexts: Set<UIOpenURLContext>) {
        guard let url = URLContexts.first?.url else { return }

        print("📦 [SceneDelegate] 수신된 URL: \(url.absoluteString)")

        // ✅ 네이버 로그인 커스텀 스킴 처리
        if url.scheme?.hasPrefix("naver") == true {
            let components = URLComponents(url: url, resolvingAgainstBaseURL: false)
            let queryItems = components?.queryItems ?? []

            func value(for key: String) -> String? {
                return queryItems.first(where: { $0.name == key })?.value
            }

            let token = value(for: "token")
            let refresh = value(for: "refresh")
            let id = value(for: "id")
            let email = value(for: "email")
            let name = value(for: "name")

            print("🪪 [SceneDelegate] 네이버 로그인 정보:")
            print("- token: \(token ?? "nil")")
            print("- refresh: \(refresh ?? "nil")")
            print("- id: \(id ?? "nil")")
            print("- email: \(email ?? "nil")")
            print("- name: \(name ?? "nil")")

            if let token = token, let refresh = refresh, let id = id {
                // ✅ 토큰 및 유저 정보 저장
                UserDefaults.standard.set(token, forKey: "accessToken")
                UserDefaults.standard.set(refresh, forKey: "refreshToken")
                UserDefaults.standard.set(id, forKey: "userId")
                UserDefaults.standard.set(email, forKey: "userEmail")
                UserDefaults.standard.set(name, forKey: "userName")

                print("✅ [SceneDelegate] 네이버 로그인 토큰 저장 완료")
                // 👉 여기선 화면 전환은 하지 않음
            } else {
                print("❌ [SceneDelegate] 필수 로그인 정보 누락: 토큰 저장 실패")
            }
        }

        // ✅ 카카오 로그인 처리
        if AuthApi.isKakaoTalkLoginUrl(url) {
            _ = AuthController.handleOpenUrl(url: url)
            print("✅ [SceneDelegate] 카카오 로그인 URL 처리 완료")
        }
    }

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let _ = (scene as? UIWindowScene) else { return }
    }

    func sceneDidDisconnect(_ scene: UIScene) {}
    func sceneDidBecomeActive(_ scene: UIScene) {}
    func sceneWillResignActive(_ scene: UIScene) {}
    func sceneWillEnterForeground(_ scene: UIScene) {}
    func sceneDidEnterBackground(_ scene: UIScene) {}
}
