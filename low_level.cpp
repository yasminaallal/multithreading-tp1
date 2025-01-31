#include <iostream>
#include <cpr/cpr.h>
#include <fstream>
#include <nlohmann/json.hpp>
#include <Eigen/Dense>
#include <chrono>

int main() {
    // Requête pour obtenir les données depuis le serveur
    std::string server_url = "http://localhost:8000";
    cpr::Response get_response = cpr::Get(cpr::Url{server_url});

    if (get_response.status_code != 200) {
        std::cerr << "Échec de la requête GET, code : " << get_response.status_code << std::endl;
        return EXIT_FAILURE;
    }

    try {
        // Analyse des données JSON reçues
        nlohmann::json received_data = nlohmann::json::parse(get_response.text);
        
        // Extraction des valeurs nécessaires
        auto matrix_values = received_data.at("a").get<std::vector<std::vector<double>>>();
        auto vector_values = received_data.at("b").get<std::vector<double>>();
        int task_id = received_data.at("identifier").get<int>();

        size_t num_rows = matrix_values.size();
        size_t num_cols = vector_values.size();

        if (num_rows == 0 || matrix_values[0].size() != num_cols) {
            std::cerr << "Erreur : dimensions incohérentes entre la matrice et le vecteur." << std::endl;
            return EXIT_FAILURE;
        }

        // Transformation en format Eigen
        Eigen::MatrixXd coefficient_matrix(num_rows, num_cols);
        for (size_t i = 0; i < num_rows; ++i) {
            for (size_t j = 0; j < num_cols; ++j) {
                coefficient_matrix(i, j) = matrix_values[i][j];
            }
        }

        Eigen::VectorXd right_hand_side(vector_values.size());
        for (size_t i = 0; i < vector_values.size(); ++i) {
            right_hand_side(i) = vector_values[i];
        }

        // Chronométrage de la résolution
        auto start_time = std::chrono::high_resolution_clock::now();
        Eigen::VectorXd solution_vector = coefficient_matrix.llt().solve(right_hand_side);
        auto end_time = std::chrono::high_resolution_clock::now();

        double execution_time = std::chrono::duration<double>(end_time - start_time).count();

        std::cout << "Tâche " << task_id << " complétée en " << execution_time << " secondes." << std::endl;

        // Création de la réponse JSON
        nlohmann::json output_json = {
            {"a", matrix_values},
            {"b", vector_values},
            {"x", solution_vector},
            {"time", execution_time},
            {"identifier", task_id}
        };

        // Envoi des résultats au serveur
        cpr::Response post_response = cpr::Post(
            cpr::Url{server_url},
            cpr::Header{{"Content-Type", "application/json"}},
            cpr::Body{output_json.dump()}
        );

        if (post_response.status_code != 200) {
            std::cerr << "Erreur lors de l'envoi des résultats : " << post_response.status_code << std::endl;
            return EXIT_FAILURE;
        }

    } catch (const std::exception& error) {
        std::cerr << "Exception capturée : " << error.what() << std::endl;
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
