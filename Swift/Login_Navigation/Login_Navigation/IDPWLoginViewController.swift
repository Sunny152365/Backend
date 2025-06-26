//
//  ViewController.swift
//  Login_Navigation
//
//  Created by 최원일 on 6/4/25.
//
// 규칙을 넣어야함

import UIKit

class IDPWLoginViewController: UIViewController {

    @IBOutlet weak var nameTextField: UITextField!
    @IBOutlet weak var emailTextField: UITextField!
    @IBOutlet weak var passwordTextField: UITextField!
    
    /// 기본적으로 생기는 네비게이션 왼쪽 아이템 숨기기
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        // 네비게이션 뒤로가기 버튼 숨기기
        self.navigationItem.hidesBackButton = true
        // 네비게이션 바 숨기기
        self.navigationController?.setNavigationBarHidden(true, animated: false)
    }

    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }

    @IBAction func BackButton2(_ sender: UIButton) {
        self.navigationController?.popViewController(animated: true)
    }
    
    func showAlert(title: String, message: String) {
        let alert = UIAlertController(title: title, message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "확인", style: .default))
        present(alert, animated: true)
    }
    
    @IBAction func signUpButtonTapped(_ sender: UIButton) {
        // 1. 빈 칸 체크
        guard let name = nameTextField.text, !name.isEmpty,
              let email = emailTextField.text, !email.isEmpty,
              let password = passwordTextField.text, !password.isEmpty else {
            showAlert(message: "모든 항목을 입력해주세요.")
            return
        }
        
        // 2. 이메일 형식 체크
        if !isValidEmail(email) {
            showAlert(message: "유효한 이메일을 입력해주세요.")
            return
        }
        
        // 3. 서버 요청 준비
        let url = URL(string: "http://172.30.1.24:8000/api/register/")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let parameters: [String: String] = [
            "name": name,
            "email": email,
            "password": password
        ]
        
        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: parameters, options: [])
        } catch {
            print("JSON 변환 에러: \(error)")
            return
        }
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("요청 실패: \(error)")
                return
            }

            if let httpResponse = response as? HTTPURLResponse {
                DispatchQueue.main.async {
                    if httpResponse.statusCode == 201 {
                        // 회원가입 성공 → 로그인 페이지로 이동
                        // self.performSegue(withIdentifier: "LoginPageViewController", sender: nil)
                        self.navigationController?.popViewController(animated: true)
                    } else {
                        if let data = data,
                           let responseStr = String(data: data, encoding: .utf8) {
                            print("서버 응답 실패: \(httpResponse.statusCode), 메시지: \(responseStr)")
                            self.showAlert(title: "회원가입 실패", message: responseStr) // 서버 메시지 그대로 보여줌
                        } else {
                            print("서버 응답 실패: \(httpResponse.statusCode)")
                            self.showAlert(title: "회원가입 실패", message: "서버 에러 코드: \(httpResponse.statusCode)")
                        }
                    }
                }
            }
        }.resume()
    }
    
    // MARK: - Helper functions
    
    func showAlert(message: String) {
        let alert = UIAlertController(title: "알림", message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "확인", style: .default))
        DispatchQueue.main.async {
            self.present(alert, animated: true)
        }
    }
    
    func isValidEmail(_ email: String) -> Bool {
        let emailRegEx = "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"
        let pred = NSPredicate(format:"SELF MATCHES %@", emailRegEx)
        return pred.evaluate(with: email)
    }

}
